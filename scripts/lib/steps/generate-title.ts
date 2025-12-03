import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription, buildSourcesPrompt } from "../prompts";

export const STEP_NAME = "generate_title";
export const TEMPERATURE = 0.1;

export function buildPrompt(ctx: ChainContext): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś kreatywnym copywriterem specjalizującym się w tytułach artykułów turystycznych.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${volume.name}

INSTRUKCJE:
- Stwórz chwytliwy, ale informatywny tytuł
- Dostosuj język do grupy docelowej
- Uwzględnij główny fokus tematyczny
- Tytuł powinien być krótki (maksymalnie 80 znaków)
- Zwróć bez cudzysłowu
- Zwróć tylko sam tytuł, bez dodatkowych komentarzy`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${volume.name}

ŹRÓDŁA INFORMACJI:
${buildSourcesPrompt(ctx.sourceArticles)}

Wygeneruj tytuł artykułu:`;

  return { system, user };
}

