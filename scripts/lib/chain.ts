import type { ChainContext, ChainResult, StepLog, GenerationLog } from "./types";
import { complete, MODEL } from "./openai";
import * as outlineStep from "./steps/generate-outline";
import * as contentStep from "./steps/generate-content";
import * as markdownStep from "./steps/format-markdown";
import * as titleStep from "./steps/generate-title";

export interface RunChainResult {
  result: ChainResult;
  log: GenerationLog;
}

export async function runChain(ctx: ChainContext): Promise<RunChainResult> {
  const generationStartedAt = new Date();
  const steps: StepLog[] = [];
  let totalInputTokens = 0;
  let totalOutputTokens = 0;

  // Step 1: Generate outline
  const outlinePrompt = outlineStep.buildPrompt(ctx);
  const outlineStartedAt = new Date();
  const outlineResult = await complete(outlinePrompt.system, outlinePrompt.user, outlineStep.TEMPERATURE);
  const outlineFinishedAt = new Date();

  steps.push({
    name: outlineStep.STEP_NAME,
    system_prompt: outlinePrompt.system,
    user_prompt: outlinePrompt.user,
    temperature: outlineStep.TEMPERATURE,
    response: outlineResult.content,
    input_tokens: outlineResult.input_tokens,
    output_tokens: outlineResult.output_tokens,
    total_tokens: outlineResult.total_tokens,
    duration_ms: outlineFinishedAt.getTime() - outlineStartedAt.getTime(),
    started_at: outlineStartedAt.toISOString(),
    finished_at: outlineFinishedAt.toISOString(),
  });
  totalInputTokens += outlineResult.input_tokens;
  totalOutputTokens += outlineResult.output_tokens;

  // Step 2: Generate content
  const contentPrompt = contentStep.buildPrompt(ctx, outlineResult.content);
  const contentStartedAt = new Date();
  const contentResult = await complete(contentPrompt.system, contentPrompt.user, contentStep.TEMPERATURE);
  const contentFinishedAt = new Date();

  steps.push({
    name: contentStep.STEP_NAME,
    system_prompt: contentPrompt.system,
    user_prompt: contentPrompt.user,
    temperature: contentStep.TEMPERATURE,
    response: contentResult.content,
    input_tokens: contentResult.input_tokens,
    output_tokens: contentResult.output_tokens,
    total_tokens: contentResult.total_tokens,
    duration_ms: contentFinishedAt.getTime() - contentStartedAt.getTime(),
    started_at: contentStartedAt.toISOString(),
    finished_at: contentFinishedAt.toISOString(),
  });
  totalInputTokens += contentResult.input_tokens;
  totalOutputTokens += contentResult.output_tokens;

  // Step 3: Format to Markdown
  const markdownPrompt = markdownStep.buildPrompt(ctx, contentResult.content);
  const markdownStartedAt = new Date();
  const markdownResult = await complete(markdownPrompt.system, markdownPrompt.user, markdownStep.TEMPERATURE);
  const markdownFinishedAt = new Date();

  steps.push({
    name: markdownStep.STEP_NAME,
    system_prompt: markdownPrompt.system,
    user_prompt: markdownPrompt.user,
    temperature: markdownStep.TEMPERATURE,
    response: markdownResult.content,
    input_tokens: markdownResult.input_tokens,
    output_tokens: markdownResult.output_tokens,
    total_tokens: markdownResult.total_tokens,
    duration_ms: markdownFinishedAt.getTime() - markdownStartedAt.getTime(),
    started_at: markdownStartedAt.toISOString(),
    finished_at: markdownFinishedAt.toISOString(),
  });
  totalInputTokens += markdownResult.input_tokens;
  totalOutputTokens += markdownResult.output_tokens;

  // Step 4: Generate title
  const titlePrompt = titleStep.buildPrompt(ctx);
  const titleStartedAt = new Date();
  const titleResult = await complete(titlePrompt.system, titlePrompt.user, titleStep.TEMPERATURE);
  const titleFinishedAt = new Date();

  steps.push({
    name: titleStep.STEP_NAME,
    system_prompt: titlePrompt.system,
    user_prompt: titlePrompt.user,
    temperature: titleStep.TEMPERATURE,
    response: titleResult.content,
    input_tokens: titleResult.input_tokens,
    output_tokens: titleResult.output_tokens,
    total_tokens: titleResult.total_tokens,
    duration_ms: titleFinishedAt.getTime() - titleStartedAt.getTime(),
    started_at: titleStartedAt.toISOString(),
    finished_at: titleFinishedAt.toISOString(),
  });
  totalInputTokens += titleResult.input_tokens;
  totalOutputTokens += titleResult.output_tokens;

  const generationFinishedAt = new Date();

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
    final_title: titleResult.content.trim(),
    final_markdown: markdownResult.content,
  };

  const result: ChainResult = {
    outline: outlineResult.content,
    content: contentResult.content,
    markdown: markdownResult.content,
    title: titleResult.content,
  };

  return { result, log };
}

