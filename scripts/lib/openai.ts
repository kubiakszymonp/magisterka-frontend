import OpenAI from "openai";
import type { ChainContext, ChainResult, StepLog, GenerationLog } from "./types";
import { CHAIN_STEPS } from "./prompts";

// === OpenAI Client (lazy) ===

export const MODEL = "gpt-4o";

let _openai: OpenAI | null = null;

function getClient(): OpenAI {
  if (!_openai) {
    _openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }
  return _openai;
}

// === API Call with logging ===

interface CompletionResult {
  content: string;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
}

async function complete(
  systemPrompt: string,
  userPrompt: string,
  temperature: number
): Promise<CompletionResult> {
  const response = await getClient().chat.completions.create({
    model: MODEL,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    temperature,
  });

  return {
    content: response.choices[0]?.message?.content ?? "",
    input_tokens: response.usage?.prompt_tokens ?? 0,
    output_tokens: response.usage?.completion_tokens ?? 0,
    total_tokens: response.usage?.total_tokens ?? 0,
  };
}

// === Chain Execution with full logging ===

export interface RunChainResult {
  result: ChainResult;
  log: GenerationLog;
}

export async function runChain(ctx: ChainContext): Promise<RunChainResult> {
  const generationStartedAt = new Date();
  const steps: StepLog[] = [];

  let totalInputTokens = 0;
  let totalOutputTokens = 0;

  const [generateOutline, generateContent, formatMarkdown, generateTitle] = CHAIN_STEPS;

  // Helper to run a step and log it
  async function runStep(
    stepDef: (typeof CHAIN_STEPS)[0],
    temperature: number,
    previousOutput?: string
  ): Promise<string> {
    const stepStartedAt = new Date();
    const fullPrompt = stepDef.prompt(ctx, previousOutput);
    const [systemPrompt, userPrompt] = fullPrompt.split("\n\n---\n\n");

    const result = await complete(systemPrompt, userPrompt, temperature);

    const stepFinishedAt = new Date();

    steps.push({
      name: stepDef.name,
      system_prompt: systemPrompt,
      user_prompt: userPrompt,
      temperature,
      response: result.content,
      input_tokens: result.input_tokens,
      output_tokens: result.output_tokens,
      total_tokens: result.total_tokens,
      duration_ms: stepFinishedAt.getTime() - stepStartedAt.getTime(),
      started_at: stepStartedAt.toISOString(),
      finished_at: stepFinishedAt.toISOString(),
    });

    totalInputTokens += result.input_tokens;
    totalOutputTokens += result.output_tokens;

    return result.content;
  }

  // Step 1: Generate outline
  const outline = await runStep(generateOutline, 0.5);

  // Step 2: Generate detailed content
  const content = await runStep(generateContent, 0.1, outline);

  // Step 3: Format to Markdown
  const markdown = await runStep(formatMarkdown, 0.1, content);

  // Step 4: Generate title
  const title = await runStep(generateTitle, 0.1);

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
    final_title: title.trim(),
    final_markdown: markdown,
  };

  return {
    result: { outline, content, markdown, title },
    log,
  };
}
