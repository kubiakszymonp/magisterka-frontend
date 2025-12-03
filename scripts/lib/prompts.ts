import type { ChainContext, SourceArticle } from "./types";

export function getAgeTargetDescription(ctx: ChainContext): { name: string; prompt: string } {
  if (ctx.variant.ageTarget === "child") {
    return {
      name: "Dzieci (8-12 lat)",
      prompt: "Używaj prostego języka, ciekawostek i angażującego tonu. Wyjaśniaj trudne pojęcia.",
    };
  }
  return {
    name: "Dorośli",
    prompt: "Używaj profesjonalnego, ale przystępnego języka. Możesz używać terminologii specjalistycznej.",
  };
}

export function getVolumeDescription(ctx: ChainContext): { name: string; prompt: string } {
  if (ctx.variant.volume === "short") {
    return {
      name: "Krótki (5 min)",
      prompt: "Skondensowana treść, tylko najważniejsze informacje. 400-600 słów.",
    };
  }
  return {
    name: "Pełny (15 min)",
    prompt: "Szczegółowy artykuł wyczerpujący temat. 1500-2000 słów.",
  };
}

export function buildSourcesPrompt(articles: SourceArticle[]): string {
  return articles
    .map((article, index) => {
      const parts = [`--- Źródło ${index + 1} ---`];
      if (article.sourceUrl) {
        parts.push(`URL: ${article.sourceUrl}`);
      }
      if (article.comment) {
        parts.push(`Komentarz: ${article.comment}`);
      }
      parts.push(`\n${article.content}`);
      return parts.join("\n");
    })
    .join("\n\n");
}
