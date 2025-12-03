import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription, buildSourcesPrompt } from "../prompts";

export const STEP_NAME = "generate_outline";
export const TEMPERATURE = 0.5;

export function buildPrompt(ctx: ChainContext): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś ekspertem w tworzeniu spisów treści dla artykułów turystycznych dostosowanych do konkretnej grupy odbiorców.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

INSTRUKCJE:
- Przeanalizuj wszystkie źródła i wybierz najciekawsze informacje
- Skup się wyłącznie na tym miejscu
- Stwórz konspekt w punktach, który jest JUŻ DOSTOSOWANY do grupy docelowej (${age.name}, ${volume.name})
- Każdy punkt powinien być konkretny i wartościowy dla tej grupy odbiorców
- Uwzględnij hierarchię ważności informacji odpowiednią dla grupy docelowej
- Dostosuj poziom szczegółowości i język do grupy wiekowej i czasu czytania
- Zwróć tylko spis treści w punktach, bez rozwinięć
- Staraj się opowiadać konkrety, bez zbędnych zaproszeń do zwiedzania i podziękowań
- Możesz na końcu podać przydatne informacje`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

ŹRÓDŁA INFORMACJI:
${buildSourcesPrompt(ctx.sourceArticles)}

Stwórz konspekt artykułu w punktach, który jest już dostosowany do grupy docelowej (${age.name}, ${volume.name}). Każdy punkt powinien zawierać krótki opis tego, co zawrzeć w akapicie, z uwzględnieniem poziomu szczegółowości i języka odpowiedniego dla tej grupy odbiorców.`;

  return { system, user };
}

