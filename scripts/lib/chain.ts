import type { ChainContext, ChainResult, StepLog, GenerationLog } from "./types";
import { complete, completeStructured, MODEL } from "./openai";
import * as outlineStep from "./steps/generate-outline";
import * as contentStep from "./steps/generate-content";
import * as markdownStep from "./steps/format-markdown";
import type { MarkdownAndTitleResponse } from "./steps/format-markdown";

export interface RunChainResult {
  result: ChainResult;
  log: GenerationLog;
}

export async function runChain(ctx: ChainContext): Promise<RunChainResult> {
  const generationStartedAt = new Date();
  const steps: StepLog[] = [];
  let totalInputTokens = 0;
  let totalOutputTokens = 0;

  const logPrefix = `      [${ctx.variant.style}]`;

  // Step 1: Generate outline
  console.log(`${logPrefix} 🔄 Krok 1/3: Generowanie konspektu...`);
  const outlinePrompt = outlineStep.buildPrompt(ctx);
  const outlineStartedAt = new Date();
  const outlineResult = await complete(outlinePrompt.system, outlinePrompt.user);
  const outlineFinishedAt = new Date();
  const outlineDuration = outlineFinishedAt.getTime() - outlineStartedAt.getTime();
  console.log(`${logPrefix} ✅ Krok 1/3: Konspekt gotowy (${outlineDuration}ms, ${outlineResult.total_tokens} tokens)`);

  steps.push({
    name: outlineStep.STEP_NAME,
    system_prompt: outlinePrompt.system,
    user_prompt: outlinePrompt.user,
    response: outlineResult.content,
    input_tokens: outlineResult.input_tokens,
    output_tokens: outlineResult.output_tokens,
    total_tokens: outlineResult.total_tokens,
    duration_ms: outlineDuration,
    started_at: outlineStartedAt.toISOString(),
    finished_at: outlineFinishedAt.toISOString(),
  });
  totalInputTokens += outlineResult.input_tokens;
  totalOutputTokens += outlineResult.output_tokens;

  // Step 2: Generate content
  console.log(`${logPrefix} 🔄 Krok 2/3: Generowanie treści...`);
  const contentPrompt = contentStep.buildPrompt(ctx, outlineResult.content);
  const contentStartedAt = new Date();
  const contentResult = await complete(contentPrompt.system, contentPrompt.user);
  const contentFinishedAt = new Date();
  const contentDuration = contentFinishedAt.getTime() - contentStartedAt.getTime();
  console.log(`${logPrefix} ✅ Krok 2/3: Treść gotowa (${contentDuration}ms, ${contentResult.total_tokens} tokens)`);

  steps.push({
    name: contentStep.STEP_NAME,
    system_prompt: contentPrompt.system,
    user_prompt: contentPrompt.user,
    response: contentResult.content,
    input_tokens: contentResult.input_tokens,
    output_tokens: contentResult.output_tokens,
    total_tokens: contentResult.total_tokens,
    duration_ms: contentDuration,
    started_at: contentStartedAt.toISOString(),
    finished_at: contentFinishedAt.toISOString(),
  });
  totalInputTokens += contentResult.input_tokens;
  totalOutputTokens += contentResult.output_tokens;

  // Step 3: Format to Markdown and generate title (structured output)
  console.log(`${logPrefix} 🔄 Krok 3/3: Formatowanie markdown + tytuł...`);
  const markdownPrompt = markdownStep.buildPrompt(ctx, contentResult.content);
  const markdownStartedAt = new Date();
  const markdownResult = await completeStructured<MarkdownAndTitleResponse>(
    markdownPrompt.system,
    markdownPrompt.user,
    markdownStep.RESPONSE_SCHEMA
  );
  const markdownFinishedAt = new Date();
  const markdownDuration = markdownFinishedAt.getTime() - markdownStartedAt.getTime();
  const markdownTokens = markdownResult.input_tokens + markdownResult.output_tokens;
  console.log(`${logPrefix} ✅ Krok 3/3: Markdown + tytuł gotowe (${markdownDuration}ms, ${markdownTokens} tokens)`);

  const { markdown, title } = markdownResult.data;

  steps.push({
    name: markdownStep.STEP_NAME,
    system_prompt: markdownPrompt.system,
    user_prompt: markdownPrompt.user,
    response: JSON.stringify(markdownResult.data),
    input_tokens: markdownResult.input_tokens,
    output_tokens: markdownResult.output_tokens,
    total_tokens: markdownTokens,
    duration_ms: markdownDuration,
    started_at: markdownStartedAt.toISOString(),
    finished_at: markdownFinishedAt.toISOString(),
  });
  totalInputTokens += markdownResult.input_tokens;
  totalOutputTokens += markdownResult.output_tokens;

  const generationFinishedAt = new Date();
  const totalDuration = generationFinishedAt.getTime() - generationStartedAt.getTime();
  console.log(`${logPrefix} 🏁 Zakończono (łącznie: ${totalDuration}ms, ${totalInputTokens + totalOutputTokens} tokens)`);

  const log: GenerationLog = {
    generated_at: generationStartedAt.toISOString(),
    place_id: ctx.placeId,
    place_name: ctx.placeName,
    style: ctx.variant.style,
    age_target: ctx.variant.ageTarget,
    volume: ctx.variant.volume,
    model: MODEL,
    source_count: ctx.sourceArticles.length,
    source_urls: ctx.sourceArticles.map((s) => s.sourceUrl),
    source_contents: ctx.sourceArticles.map((s) => s.content),
    source_comments: ctx.sourceArticles.map((s) => s.comment),
    total_duration_ms: generationFinishedAt.getTime() - generationStartedAt.getTime(),
    total_input_tokens: totalInputTokens,
    total_output_tokens: totalOutputTokens,
    total_tokens: totalInputTokens + totalOutputTokens,
    steps,
    final_title: title.trim(),
    final_markdown: markdown,
  };

  const result: ChainResult = {
    outline: outlineResult.content,
    content: contentResult.content,
    markdown: markdown,
    title: title,
  };

  return { result, log };
}

