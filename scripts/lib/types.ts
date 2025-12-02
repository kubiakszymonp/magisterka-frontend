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
  sourceContent: string;
  variant: ArticleVariant;
}

export interface ChainStep {
  name: string;
  prompt: (ctx: ChainContext, previousOutput?: string) => string;
}

export interface ChainResult {
  outline: string;
  content: string;
  markdown: string;
  title: string;
}

