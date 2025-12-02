import OpenAI from "openai";
import type { ChainContext, ChainResult } from "./types";
import { CHAIN_STEPS } from "./prompts";

// === OpenAI Client (lazy) ===

const MODEL = "gpt-5-nano"; // zmień na gpt-5-nano gdy dostępny

let _openai: OpenAI | null = null;

function getClient(): OpenAI {
  if (!_openai) {
    _openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }
  return _openai;
}

// === API Call ===

async function complete(prompt: string, temperature = 0.7): Promise<string> {
  const [systemPrompt, userPrompt] = prompt.split("\n\n---\n\n");

  const response = await getClient().chat.completions.create({
    model: MODEL,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    temperature,
  });

  return response.choices[0]?.message?.content ?? "";
}

// === Chain Execution ===

export async function runChain(ctx: ChainContext): Promise<ChainResult> {
  const [generateOutline, generateContent, formatMarkdown, generateTitle] = CHAIN_STEPS;

  // Step 1: Generate outline
  const outlinePrompt = generateOutline.prompt(ctx);
  const outline = await complete(outlinePrompt, 0.5);

  // Step 2: Generate detailed content
  const contentPrompt = generateContent.prompt(ctx, outline);
  const content = await complete(contentPrompt, 0.1);

  // Step 3: Format to Markdown
  const markdownPrompt = formatMarkdown.prompt(ctx, content);
  const markdown = await complete(markdownPrompt, 0.1);

  // Step 4: Generate title
  const titlePrompt = generateTitle.prompt(ctx);
  const title = await complete(titlePrompt, 0.1);

  return { outline, content, markdown, title };
}

// === Dry Run (bez API) ===

export function dryRunChain(ctx: ChainContext): void {
  console.log("\n=== DRY RUN ===\n");

  for (const step of CHAIN_STEPS) {
    console.log(`--- ${step.name} ---`);
    console.log(step.prompt(ctx, "[previous output]").slice(0, 200) + "...\n");
  }
}

