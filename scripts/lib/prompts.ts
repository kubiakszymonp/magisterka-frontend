import type { ChainContext, ChainStep } from "./types";

// === Style Descriptions ===

function getAgeTargetDescription(ctx: ChainContext): { name: string; prompt: string } {
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

function getTimeTargetDescription(ctx: ChainContext): { name: string; prompt: string } {
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

function buildContextPrompt(ctx: ChainContext, instruction: string): string {
  const age = getAgeTargetDescription(ctx);
  const time = getTimeTargetDescription(ctx);

  return `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${time.name}

ŹRÓDŁA INFORMACJI:
${ctx.sourceContent}

${instruction}`;
}

// === Chain Steps ===

export const CHAIN_STEPS: ChainStep[] = [
  {
    name: "generate_outline",
    prompt: (ctx) => {
      const age = getAgeTargetDescription(ctx);
      const time = getTimeTargetDescription(ctx);

      const systemPrompt = `Jesteś ekspertem w tworzeniu spisów treści dla artykułów turystycznych.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${time.name} - ${time.prompt}

INSTRUKCJE:
- Przeanalizuj wszystkie źródła i wybierz najciekawsze informacje
- Skup się wyłącznie na tym miejscu
- Stwórz konspekt w punktach pasujący do kategorii docelowych
- Każdy punkt powinien być konkretny i wartościowy
- Uwzględnij hierarchię ważności informacji
- Zwróć tylko spis treści w punktach, bez rozwinięć
- Staraj się opowiadać konkrety, bez zbędnych zaproszeń do zwiedzania i podziękowań
- Możesz na końcu podać przydatne informacje`;

      const userPrompt = buildContextPrompt(ctx, "Stwórz spis treści artykułu w punktach, wraz z krótkim opisem co zawrzeć w akapicie.");

      return `${systemPrompt}\n\n---\n\n${userPrompt}`;
    },
  },

  {
    name: "generate_content",
    prompt: (ctx, outline) => {
      const age = getAgeTargetDescription(ctx);
      const time = getTimeTargetDescription(ctx);

      const systemPrompt = `Jesteś ekspertem przewodnikiem turystycznym. Twoją rolą jest stworzenie szczegółowych opisów dla każdego punktu z konspektu.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${time.name} - ${time.prompt}

INSTRUKCJE:
- Rozwiń każdy punkt z konspektu w szczegółowy opis
- Dostosuj objętość do kategorii czasowej, ale staraj się rozpoczęte wątki kończyć w sposób pełny, nie pozostawiając niedomówień
- Bazuj na źródłach, ale twórz płynny tekst
- Zachowaj merytoryczność i dokładność
- Jeżeli pojawiają się jakieś nawiązania kulturowe albo do postaci, to je krótko opisz, żeby czytelnik złapał kontekst
- Artykuł ma być informatywny i kompletny, żeby nikt nie musiał się później zastanawiać o co chodzi
- NIE UŻYWAJ FORMATOWANIA MARKDOWN - tylko czysty tekst`;

      const userPrompt = buildContextPrompt(ctx, `Konspekt do rozwinięcia:\n${outline}\n\nStwórz szczegółowe opisy dla każdego punktu:`);

      return `${systemPrompt}\n\n---\n\n${userPrompt}`;
    },
  },

  {
    name: "format_markdown",
    prompt: (ctx, content) => {
      const age = getAgeTargetDescription(ctx);
      const time = getTimeTargetDescription(ctx);

      const systemPrompt = `Jesteś redaktorem specjalizującym się w formatowaniu artykułów turystycznych do Markdown.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${time.name} - ${time.prompt}

INSTRUKCJE:
- Przekształć tekst w czysty format Markdown
- Dodaj odpowiednie nagłówki (# ## ###)
- Użyj pogrubień (**tekst**) dla ważnych informacji
- Dodaj kursywę (*tekst*) dla ciekawostek
- Stwórz listy punktowane gdzie pasuje
- Dostosuj język do grupy docelowej
- Upewnij się, że tekst jest płynny i czytelny
- NIE DODAWAJ TYTUŁU - zacznij od treści`;

      const userPrompt = `Tekst do sformatowania:\n\n${content}\n\nPrzekształć w czysty format Markdown:`;

      return `${systemPrompt}\n\n---\n\n${userPrompt}`;
    },
  },

  {
    name: "generate_title",
    prompt: (ctx) => {
      const age = getAgeTargetDescription(ctx);
      const time = getTimeTargetDescription(ctx);

      const systemPrompt = `Jesteś kreatywnym copywriterem specjalizującym się w tytułach artykułów turystycznych.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${time.name}

INSTRUKCJE:
- Stwórz chwytliwy, ale informatywny tytuł
- Dostosuj język do grupy docelowej
- Uwzględnij główny fokus tematyczny
- Tytuł powinien być krótki (maksymalnie 80 znaków)
- Zwróć bez cudzysłowu
- Zwróć tylko sam tytuł, bez dodatkowych komentarzy`;

      const userPrompt = buildContextPrompt(ctx, "Wygeneruj tytuł artykułu:");

      return `${systemPrompt}\n\n---\n\n${userPrompt}`;
    },
  },
];
