import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription } from "../prompts";

export const STEP_NAME = "format_markdown_and_title";
export const TEMPERATURE = 0.1;

export interface MarkdownAndTitleResponse {
  markdown: string;
  title: string;
}

export const RESPONSE_SCHEMA = {
  name: "markdown_and_title",
  schema: {
    type: "object",
    properties: {
      markdown: {
        type: "string",
        description: "Artykuł sformatowany w Markdown (bez tytułu)",
      },
      title: {
        type: "string",
        description: "Chwytliwy tytuł artykułu (maksymalnie 80 znaków)",
      },
    },
    required: ["markdown", "title"],
    additionalProperties: false,
  },
};

export function buildPrompt(ctx: ChainContext, content: string): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś redaktorem specjalizującym się w formatowaniu artykułów turystycznych do Markdown i tworzeniu tytułów.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

INSTRUKCJE:
- Przekształć tekst w czysty format Markdown
- Dodaj odpowiednie nagłówki (## ###)
- Użyj pogrubień (**tekst**) dla ważnych informacji
- Dodaj kursywę (*tekst*) dla ciekawostek
- Stwórz listy punktowane gdzie pasuje
- Upewnij się, że tekst jest płynny i czytelny
- Stwórz chwytliwy, informatywny tytuł dostosowany do grupy docelowej (${age.name})
- Tytuł powinien być krótki (maksymalnie 80 znaków)`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${volume.name}

Tekst do sformatowania:

${content}

Przekształć w czysty format Markdown i stwórz tytuł.`;

  return { system, user };
}

