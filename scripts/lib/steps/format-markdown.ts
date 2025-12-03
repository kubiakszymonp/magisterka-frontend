import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription } from "../prompts";

export const STEP_NAME = "format_markdown";
export const TEMPERATURE = 0.1;

export function buildPrompt(ctx: ChainContext, content: string): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś redaktorem specjalizującym się w formatowaniu artykułów turystycznych do Markdown.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

INSTRUKCJE:
- Przekształć tekst w czysty format Markdown
- Dodaj odpowiednie nagłówki (# ## ###)
- Użyj pogrubień (**tekst**) dla ważnych informacji
- Dodaj kursywę (*tekst*) dla ciekawostek
- Stwórz listy punktowane gdzie pasuje
- Dostosuj język do grupy docelowej
- Upewnij się, że tekst jest płynny i czytelny
- NIE DODAWAJ TYTUŁU - zacznij od treści`;

  const user = `Tekst do sformatowania:

${content}

Przekształć w czysty format Markdown:`;

  return { system, user };
}

