import OpenAI from "openai";

export const MODEL = "gpt-5-mini";

let _client: OpenAI | null = null;

function getClient(): OpenAI {
  if (!_client) {
    _client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }
  return _client;
}

export interface CompletionResult {
  content: string;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
}

export async function complete(
  systemPrompt: string,
  userPrompt: string
): Promise<CompletionResult> {
  const response = await getClient().chat.completions.create({
    model: MODEL,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
  });

  return {
    content: response.choices[0]?.message?.content ?? "",
    input_tokens: response.usage?.prompt_tokens ?? 0,
    output_tokens: response.usage?.completion_tokens ?? 0,
    total_tokens: response.usage?.total_tokens ?? 0,
  };
}

export interface StructuredCompletionResult<T> {
  data: T;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
}

export async function completeStructured<T>(
  systemPrompt: string,
  userPrompt: string,
  schema: {
    name: string;
    schema: Record<string, unknown>;
  }
): Promise<StructuredCompletionResult<T>> {
  const response = await getClient().chat.completions.create({
    model: MODEL,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    response_format: {
      type: "json_schema",
      json_schema: {
        name: schema.name,
        strict: true,
        schema: schema.schema,
      },
    },
  });

  const content = response.choices[0]?.message?.content ?? "{}";
  const data = JSON.parse(content) as T;

  return {
    data,
    input_tokens: response.usage?.prompt_tokens ?? 0,
    output_tokens: response.usage?.completion_tokens ?? 0,
    total_tokens: response.usage?.total_tokens ?? 0,
  };
}
