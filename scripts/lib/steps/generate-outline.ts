import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription, buildSourcesPrompt } from "../prompts";

export const STEP_NAME = "generate_outline";
export const TEMPERATURE = 0.5;

export function buildPrompt(ctx: ChainContext): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś ekspertem w tworzeniu spisów treści dla artykułów turystycznych.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

INSTRUKCJE:
- Przeanalizuj wszystkie źródła i wybierz najciekawsze informacje
- Skup się wyłącznie na tym miejscu
- Stwórz konspekt w punktach pasujący do kategorii docelowych
- Każdy punkt powinien być konkretny i wartościowy
- Uwzględnij hierarchię ważności informacji
- Zwróć tylko spis treści w punktach, bez rozwinięć
- Staraj się opowiadać konkrety, bez zbędnych zaproszeń do zwiedzania i podziękowań
- Możesz na końcu podać przydatne informacje`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${volume.name}

ŹRÓDŁA INFORMACJI:
${buildSourcesPrompt(ctx.sourceArticles)}

Stwórz spis treści artykułu w punktach, wraz z krótkim opisem co zawrzeć w akapicie.`;

  return { system, user };
}

