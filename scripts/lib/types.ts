// === Data Types ===

export interface Place {
  id: string;
  name: string;
  thumbnail: string;
  description: string;
}

export interface SourceArticle {
  sourceUrl: string;
  content: string;
  comment: string;
}

export interface GeneratedArticle {
  placeId: string;
  style: string;
  ageTarget: AgeTarget;
  volume: Volume;
  title: string;
  content: string;
}

// === Generation Types ===

export type AgeTarget = "adult" | "child";
export type Volume = "full" | "short";

export interface ArticleVariant {
  style: string;
  ageTarget: AgeTarget;
  volume: Volume;
}

export const VARIANTS: ArticleVariant[] = [
  { style: "adult_full", ageTarget: "adult", volume: "full" },
  { style: "adult_short", ageTarget: "adult", volume: "short" },
  { style: "child_short", ageTarget: "child", volume: "short" },
];

// === Chain Types ===

export interface ChainContext {
  placeName: string;
  placeId: string;
  sourceArticles: SourceArticle[];
  variant: ArticleVariant;
}

export interface ChainResult {
  outline: string;
  content: string;
  markdown: string;
  title: string;
}

// === Generation Log (for research) ===

export interface StepLog {
  name: string;
  system_prompt: string;
  user_prompt: string;
  response: string;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  duration_ms: number;
  started_at: string;
  finished_at: string;
}

export interface GenerationLog {
  generated_at: string;
  place_id: string;
  place_name: string;
  style: string;
  age_target: AgeTarget;
  volume: Volume;
  model: string;
  source_count: number;
  source_urls: string[];
  source_contents: string[];
  source_comments: string[];
  total_duration_ms: number;
  total_input_tokens: number;
  total_output_tokens: number;
  total_tokens: number;
  steps: StepLog[];
  final_title: string;
  final_markdown: string;
}

