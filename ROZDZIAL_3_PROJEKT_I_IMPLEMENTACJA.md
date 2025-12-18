# 3. Projekt i implementacja systemu generacji artykułów

## 3.1 Źródła danych (3 artykuły źródłowe)

System generacji artykułów wykorzystuje trzy artykuły źródłowe jako podstawę do tworzenia treści. Każde miejsce (place) ma przypisany zestaw trzech artykułów źródłowych, które są przechowywane w formacie JSON w katalogu `data/source-articles/`.

### Struktura danych źródłowych

Artykuły źródłowe są przechowywane w plikach JSON, gdzie nazwa pliku odpowiada identyfikatorowi miejsca (placeId). Każdy plik zawiera tablicę trzech obiektów `SourceArticle`, z których każdy reprezentuje jedno źródło:

```typescript
interface SourceArticle {
  sourceUrl: string;    // URL źródła (np. strona internetowa, Wikipedia)
  content: string;       // Treść artykułu źródłowego
  comment: string;       // Opcjonalny komentarz do źródła
}
```

### Przykład struktury danych

Dla miejsca `ratusz_w_kaliszu` plik `data/source-articles/ratusz_w_kaliszu.json` zawiera trzy artykuły:

```json
[
  {
    "sourceUrl": "https://www.kalisz.info/ratusz.html",
    "content": "Najwcześniejsza wiadomość o kaliskiej siedzibie...",
    "comment": ""
  },
  {
    "sourceUrl": "https://www.kalisz.pl/dla-turysty/zabytki/ratusz,3",
    "content": "Ratusz to siedziba władz miejskich...",
    "comment": ""
  },
  {
    "sourceUrl": "https://pl.wikipedia.org/wiki/Ratusz_w_Kaliszu",
    "content": "Ratusz w Kaliszu – ratusz w Śródmieściu...",
    "comment": ""
  }
]
```

### Ładowanie źródeł

Funkcja `loadSourceArticles()` w module `scripts/lib/files.ts` odpowiada za wczytanie artykułów źródłowych dla danego miejsca:

```21:30:scripts/lib/files.ts
export function loadSourceArticles(placeId: string): SourceArticle[] {
  const filePath = path.join(SOURCE_ARTICLES_DIR, `${placeId}.json`);

  if (!fs.existsSync(filePath)) {
    return [];
  }

  const content = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(content);
}
```

Artykuły źródłowe są następnie formatowane do promptów dla modelu językowego za pomocą funkcji `buildSourcesPrompt()`, która łączy wszystkie trzy źródła w jeden spójny tekst z wyraźnym oznaczeniem każdego źródła:

```29:43:scripts/lib/prompts.ts
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
```

### Wykorzystanie źródeł w procesie generacji

Wszystkie trzy artykuły źródłowe są przekazywane do każdego kroku pipeline'u generacji jako kontekst. Model językowy jest instruowany, aby bazował wyłącznie na informacjach zawartych w tych źródłach, co zapewnia wiarygodność i spójność generowanych treści.

## 3.2 Pipeline generacji

Pipeline generacji artykułów składa się z trzech sekwencyjnych kroków, które przekształcają źródłowe artykuły w gotowy artykuł dostosowany do określonego stylu i grupy docelowej. Każdy krok wykorzystuje model językowy GPT-5-nano do przetwarzania danych.

### Architektura pipeline'u

Główna funkcja `runChain()` w module `scripts/lib/chain.ts` koordynuje cały proces generacji:

```13:133:scripts/lib/chain.ts
export async function runChain(ctx: ChainContext): Promise<RunChainResult> {
  const generationStartedAt = new Date();
  const steps: StepLog[] = [];
  let totalInputTokens = 0;
  let totalOutputTokens = 0;

  const logPrefix = `      [${ctx.variant.style}]`;

  // Step 1: Generate outline
  console.log(`${logPrefix} 🔄 Krok 1/3: Generowanie konspektu...`);
  const outlinePrompt = outlineStep.buildPrompt(ctx);
  const outlineStartedAt = new Date();
  const outlineResult = await complete(outlinePrompt.system, outlinePrompt.user);
  const outlineFinishedAt = new Date();
  const outlineDuration = outlineFinishedAt.getTime() - outlineStartedAt.getTime();
  console.log(`${logPrefix} ✅ Krok 1/3: Konspekt gotowy (${outlineDuration}ms, ${outlineResult.total_tokens} tokens)`);

  steps.push({
    name: outlineStep.STEP_NAME,
    system_prompt: outlinePrompt.system,
    user_prompt: outlinePrompt.user,
    response: outlineResult.content,
    input_tokens: outlineResult.input_tokens,
    output_tokens: outlineResult.output_tokens,
    total_tokens: outlineResult.total_tokens,
    duration_ms: outlineDuration,
    started_at: outlineStartedAt.toISOString(),
    finished_at: outlineFinishedAt.toISOString(),
  });
  totalInputTokens += outlineResult.input_tokens;
  totalOutputTokens += outlineResult.output_tokens;

  // Step 2: Generate content
  console.log(`${logPrefix} 🔄 Krok 2/3: Generowanie treści...`);
  const contentPrompt = contentStep.buildPrompt(ctx, outlineResult.content);
  const contentStartedAt = new Date();
  const contentResult = await complete(contentPrompt.system, contentPrompt.user);
  const contentFinishedAt = new Date();
  const contentDuration = contentFinishedAt.getTime() - contentStartedAt.getTime();
  console.log(`${logPrefix} ✅ Krok 2/3: Treść gotowa (${contentDuration}ms, ${contentResult.total_tokens} tokens)`);

  steps.push({
    name: contentStep.STEP_NAME,
    system_prompt: contentPrompt.system,
    user_prompt: contentPrompt.user,
    response: contentResult.content,
    input_tokens: contentResult.input_tokens,
    output_tokens: contentResult.output_tokens,
    total_tokens: contentResult.total_tokens,
    duration_ms: contentDuration,
    started_at: contentStartedAt.toISOString(),
    finished_at: contentFinishedAt.toISOString(),
  });
  totalInputTokens += contentResult.input_tokens;
  totalOutputTokens += contentResult.output_tokens;

  // Step 3: Format to Markdown and generate title (structured output)
  console.log(`${logPrefix} 🔄 Krok 3/3: Formatowanie markdown + tytuł...`);
  const markdownPrompt = markdownStep.buildPrompt(ctx, contentResult.content);
  const markdownStartedAt = new Date();
  const markdownResult = await completeStructured<MarkdownAndTitleResponse>(
    markdownPrompt.system,
    markdownPrompt.user,
    markdownStep.RESPONSE_SCHEMA
  );
  const markdownFinishedAt = new Date();
  const markdownDuration = markdownFinishedAt.getTime() - markdownStartedAt.getTime();
  const markdownTokens = markdownResult.input_tokens + markdownResult.output_tokens;
  console.log(`${logPrefix} ✅ Krok 3/3: Markdown + tytuł gotowe (${markdownDuration}ms, ${markdownTokens} tokens)`);

  const { markdown, title } = markdownResult.data;

  steps.push({
    name: markdownStep.STEP_NAME,
    system_prompt: markdownPrompt.system,
    user_prompt: markdownPrompt.user,
    response: JSON.stringify(markdownResult.data),
    input_tokens: markdownResult.input_tokens,
    output_tokens: markdownResult.output_tokens,
    total_tokens: markdownTokens,
    duration_ms: markdownDuration,
    started_at: markdownStartedAt.toISOString(),
    finished_at: markdownFinishedAt.toISOString(),
  });
  totalInputTokens += markdownResult.input_tokens;
  totalOutputTokens += markdownResult.output_tokens;

  const generationFinishedAt = new Date();
  const totalDuration = generationFinishedAt.getTime() - generationStartedAt.getTime();
  console.log(`${logPrefix} 🏁 Zakończono (łącznie: ${totalDuration}ms, ${totalInputTokens + totalOutputTokens} tokens)`);

  const log: GenerationLog = {
    generated_at: generationStartedAt.toISOString(),
    place_id: ctx.placeId,
    place_name: ctx.placeName,
    style: ctx.variant.style,
    age_target: ctx.variant.ageTarget,
    volume: ctx.variant.volume,
    model: MODEL,
    source_count: ctx.sourceArticles.length,
    source_urls: ctx.sourceArticles.map((s) => s.sourceUrl),
    source_contents: ctx.sourceArticles.map((s) => s.content),
    source_comments: ctx.sourceArticles.map((s) => s.comment),
    total_duration_ms: generationFinishedAt.getTime() - generationStartedAt.getTime(),
    total_input_tokens: totalInputTokens,
    total_output_tokens: totalOutputTokens,
    total_tokens: totalInputTokens + totalOutputTokens,
    steps,
    final_title: title.trim(),
    final_markdown: markdown,
  };

  const result: ChainResult = {
    outline: outlineResult.content,
    content: contentResult.content,
    markdown: markdown,
    title: title,
  };

  return { result, log };
}
```

Każdy krok jest wykonywany sekwencyjnie, a wyniki poprzedniego kroku są wykorzystywane jako wejście do następnego. System loguje szczegółowe informacje o każdym kroku, w tym czas wykonania, liczbę tokenów wejściowych i wyjściowych, oraz pełne prompty i odpowiedzi.

### 3.2.1 Krok 1: konspekt

Pierwszy krok pipeline'u generuje konspekt (outline) artykułu na podstawie trzech artykułów źródłowych. Konspekt jest już dostosowany do docelowej grupy odbiorców (wiek i objętość).

#### Implementacja

Moduł `scripts/lib/steps/generate-outline.ts` odpowiada za generowanie konspektu:

```6:39:scripts/lib/steps/generate-outline.ts
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
- Przyjmij, że czytelnik już jest w tym miejscu, a ty jesteś jego przewodnikiem.
- Stwórz konspekt w punktach, który jest JUŻ DOSTOSOWANY do grupy docelowej (${age.name}, ${volume.name})
- Każdy punkt powinien być konkretny i wartościowy dla tej grupy odbiorców
- Uwzględnij hierarchię ważności informacji odpowiednią dla grupy docelowej
- Dostosuj poziom szczegółowości i język do grupy wiekowej i czasu czytania
- Zwróć tylko spis treści w punktach, bez rozwinięć
- Staraj się opowiadać konkrety, bez zbędnych zaproszeń do zwiedzania i podziękowań`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

ŹRÓDŁA INFORMACJI:
${buildSourcesPrompt(ctx.sourceArticles)}

Stwórz konspekt artykułu w punktach, który jest już dostosowany do grupy docelowej (${age.name}, ${volume.name}). Każdy punkt powinien zawierać krótki opis tego, co zawrzeć w akapicie, z uwzględnieniem poziomu szczegółowości i języka odpowiedniego dla tej grupy odbiorców.`;

  return { system, user };
}
```

#### Charakterystyka konspektu

Konspekt jest generowany z uwzględnieniem:
- **Grupy wiekowej**: Dla dzieci konspekt zawiera więcej ciekawostek i prostszych pojęć, dla dorosłych może zawierać terminologię specjalistyczną
- **Objętości**: Dla wersji krótkiej konspekt jest bardziej skondensowany, dla pełnej - bardziej szczegółowy
- **Hierarchii informacji**: Najważniejsze informacje są umieszczone na początku konspektu

Konspekt jest zwracany jako zwykły tekst w formacie punktów, bez formatowania markdown, ponieważ służy jako wejście do następnego kroku.

### 3.2.2 Krok 2: generacja surowego artykułu

Drugi krok rozwija konspekt w pełny tekst artykułu. Model otrzymuje konspekt z pierwszego kroku oraz wszystkie trzy artykuły źródłowe i generuje szczegółowe opisy dla każdego punktu konspektu.

#### Implementacja

Moduł `scripts/lib/steps/generate-content.ts` odpowiada za generowanie treści:

```6:42:scripts/lib/steps/generate-content.ts
export function buildPrompt(ctx: ChainContext, outline: string): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś ekspertem przewodnikiem turystycznym. Twoją rolą jest stworzenie szczegółowych opisów dla każdego punktu z konspektu w języku docelowym dostosowanym do grupy odbiorców.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

INSTRUKCJE:
- Rozwiń każdy punkt z konspektu w szczegółowy opis
- Przyjmij, że czytelnik już jest w tym miejscu, a ty jesteś jego przewodnikiem
- Użyj języka docelowego zgodnego z grupą odbiorców (${age.name})
- Dostosuj objętość do kategorii czasowej, ale staraj się rozpoczęte wątki kończyć w sposób pełny, nie pozostawiając niedomówień
- Twórz płynny tekst w docelowym języku
- Zachowaj merytoryczność i dokładność
- Jeżeli pojawiają się jakieś nawiązania kulturowe albo do postaci, to je krótko opisz, żeby czytelnik złapał kontekst
- Artykuł ma być informatywny i kompletny, żeby nikt nie musiał się później zastanawiać o co chodzi
- NIE UŻYWAJ FORMATOWANIA MARKDOWN - tylko czysty tekst`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

ŹRÓDŁA INFORMACJI (bazuj TYLKO na tych danych):
${buildSourcesPrompt(ctx.sourceArticles)}

Konspekt do rozwinięcia (już dostosowany do grupy docelowej):
${outline}

Stwórz szczegółowe opisy dla każdego punktu w języku docelowym zgodnym z grupą odbiorców (${age.name}), bazując wyłącznie na danych ze źródeł:`;

  return { system, user };
}
```

#### Charakterystyka generowanej treści

Wygenerowany tekst:
- Jest napisany w języku docelowym dostosowanym do grupy wiekowej
- Ma odpowiednią objętość (400-600 słów dla krótkich, 1000-1200 dla pełnych)
- Bazuje wyłącznie na informacjach z trzech artykułów źródłowych
- Jest płynny i czytelny, bez formatowania markdown
- Zawiera wyjaśnienia kontekstu kulturowego i historycznego tam, gdzie to potrzebne

### 3.2.3 Krok 3: transformacja do stylów

Trzeci krok przekształca surowy tekst w sformatowany artykuł Markdown z tytułem. Wykorzystuje structured output API OpenAI, aby zapewnić poprawny format odpowiedzi.

#### Implementacja

Moduł `scripts/lib/steps/format-markdown.ts` odpowiada za formatowanie:

```30:62:scripts/lib/steps/format-markdown.ts
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
```

#### Structured Output

Krok trzeci wykorzystuje structured output API, które zapewnia, że odpowiedź jest zawsze w poprawnym formacie JSON:

```11:28:scripts/lib/steps/format-markdown.ts
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
```

Funkcja `completeStructured()` w module `scripts/lib/openai.ts` obsługuje wywołanie z structured output:

```48:81:scripts/lib/openai.ts
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
```

#### Formatowanie Markdown

Wygenerowany artykuł Markdown zawiera:
- Nagłówki drugiego i trzeciego poziomu (##, ###) dla strukturyzacji treści
- Pogrubienia (**tekst**) dla ważnych informacji
- Listy punktowane tam, gdzie to pasuje
- Płynny, czytelny tekst dostosowany do grupy docelowej

Tytuł jest generowany osobno i jest dostosowany do grupy wiekowej - dla dzieci jest bardziej angażujący, dla dorosłych bardziej informatywny.

## 3.3 Opis stylów (dorośli pełny / skrót / dzieci)

System generuje trzy warianty artykułów dla każdego miejsca, różniące się grupą docelową (wiek) i objętością (czas czytania). Każdy wariant jest identyfikowany przez unikalny styl (style).

### Definicja wariantów

Warianty są zdefiniowane w module `scripts/lib/types.ts`:

```36:40:scripts/lib/types.ts
export const VARIANTS: ArticleVariant[] = [
  { style: "adult_full", ageTarget: "adult", volume: "full" },
  { style: "adult_short", ageTarget: "adult", volume: "short" },
  { style: "child_short", ageTarget: "child", volume: "short" },
];
```

### Wariant 1: Dorośli – pełny (adult_full)

**Charakterystyka:**
- **Grupa docelowa**: Dorośli
- **Czas czytania**: 10 minut
- **Objętość**: 1000-1200 słów
- **Język**: Profesjonalny, ale przystępny, z możliwością użycia terminologii specjalistycznej
- **Poziom szczegółowości**: Wysoki - artykuł wyczerpuje temat

**Przykładowe użycie**: Dla użytkowników, którzy chcą poznać miejsce w pełni, z wszystkimi szczegółami historycznymi i architektonicznymi.

### Wariant 2: Dorośli – skrót (adult_short)

**Charakterystyka:**
- **Grupa docelowa**: Dorośli
- **Czas czytania**: 5 minut
- **Objętość**: 400-600 słów
- **Język**: Profesjonalny, ale przystępny
- **Poziom szczegółowości**: Średni - tylko najważniejsze informacje

**Przykładowe użycie**: Dla użytkowników, którzy chcą szybko zapoznać się z miejscem, bez wchodzenia w szczegóły.

### Wariant 3: Dzieci – skrót (child_short)

**Charakterystyka:**
- **Grupa docelowa**: Dzieci w wieku 8-12 lat
- **Czas czytania**: 5 minut
- **Objętość**: 400-600 słów
- **Język**: Prosty, z ciekawostkami i angażującym tonem, wyjaśnieniami trudnych pojęć
- **Poziom szczegółowości**: Niski - skupia się na ciekawostkach i angażujących historiach

**Przykładowe użycie**: Dla dzieci, które zwiedzają miejsce z rodzicami i potrzebują zrozumiałego, interesującego opisu.

### Dostosowanie promptów do stylów

Funkcje `getAgeTargetDescription()` i `getVolumeDescription()` w module `scripts/lib/prompts.ts` generują odpowiednie opisy dla każdego wariantu:

```3:27:scripts/lib/prompts.ts
export function getAgeTargetDescription(ctx: ChainContext): { name: string; prompt: string } {
  if (ctx.variant.ageTarget === "child") {
    return {
      name: "Dzieci (8-12 lat)",
      prompt: "Używaj prostego języka, ciekawostek i angażującego tonu. Wyjaśniaj trudne pojęcia. Masz opowiadać ciekawie jak do dzieci, aby je zachęcić i zainteresować.",
    };
  }
  return {
    name: "Dorośli",
    prompt: "Używaj profesjonalnego, ale przystępnego języka. Możesz używać terminologii specjalistycznej. wyjaśniaj złożone zjawiska.",
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
    name: "Pełny (10 min)",
    prompt: "Szczegółowy artykuł wyczerpujący temat. Maksymalnie 1000-1200 słów.",
  };
}
```

Te opisy są następnie wykorzystywane we wszystkich trzech krokach pipeline'u, zapewniając spójne dostosowanie treści do wybranego stylu.

### Generowanie wszystkich wariantów

Dla każdego miejsca system generuje wszystkie trzy warianty równolegle:

```30:65:scripts/process-articles.ts
async function processPlace(placeId: string, placeName: string, sourceArticles: SourceArticle[]): Promise<number> {
  const tag = `[${placeName}]`;
  console.log(`${tag} → Generowanie ${VARIANTS.length} wariantów...`);

  const results = await Promise.all(
    VARIANTS.map(async (variant) => {
      const ctx: ChainContext = {
        placeId,
        placeName,
        sourceArticles,
        variant,
      };

      const { result, log } = await runChain(ctx);

      const article: GeneratedArticle = {
        placeId,
        style: variant.style,
        ageTarget: variant.ageTarget,
        volume: variant.volume,
        title: result.title.trim(),
        content: result.markdown,
      };

      saveArticle(article);
      saveGenerationLog(log);

      console.log(`${tag} ✓ ${variant.style}: ${log.total_tokens} tokens, ${log.total_duration_ms}ms`);

      return log;
    })
  );

  console.log(`${tag} ✅ Zakończono (${results.length} wariantów)`);
  return results.length;
}
```

Równoległe przetwarzanie przyspiesza generowanie, ponieważ każdy wariant jest niezależny i może być generowany jednocześnie.

## 3.4 Struktura aplikacji webowej (Next.js)

Aplikacja webowa jest zbudowana w oparciu o framework Next.js 16 z wykorzystaniem App Router. Aplikacja prezentuje wygenerowane artykuły użytkownikom i umożliwia zbieranie opinii.

### Architektura Next.js

Next.js wykorzystuje App Router, gdzie struktura katalogów w `app/` definiuje routing aplikacji. Główne komponenty aplikacji:

```
app/
├── api/                    # API routes (backend)
│   ├── articles/          # Endpointy do pobierania artykułów
│   ├── places/            # Endpointy do pobierania miejsc
│   ├── rate-single/       # Endpoint do zapisywania ocen pojedynczych
│   └── rate-compare/       # Endpoint do zapisywania ocen porównawczych
├── places/                 # Strony związane z miejscami
│   └── [placeId]/         # Dynamiczny routing dla miejsc
│       ├── page.tsx       # Strona główna miejsca (lista wariantów)
│       ├── [style]/       # Dynamiczny routing dla stylów
│       │   └── page.tsx   # Strona pojedynczego artykułu
│       └── compare/       # Strona porównania wariantów
│           └── page.tsx
├── layout.tsx             # Główny layout aplikacji
├── page.tsx               # Strona główna (lista miejsc)
└── globals.css            # Globalne style
```

### API Routes

Aplikacja wykorzystuje Next.js API Routes do obsługi zapytań backendowych. Wszystkie endpointy są zdefiniowane w katalogu `app/api/`.

#### Endpoint artykułów

Endpoint `/api/articles/[placeId]/[style]` zwraca artykuł dla danego miejsca i stylu:

```7:28:app/api/articles/[placeId]/[style]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ placeId: string; style: string }> }
) {
  const { placeId, style } = await params;

  try {
    // New structure: data/articles/{placeId}/{style}.json
    const filePath = path.join(
      process.cwd(),
      "data",
      "articles",
      placeId,
      `${style}.json`
    );
    const fileContents = fs.readFileSync(filePath, "utf8");
    const article = JSON.parse(fileContents);
    return NextResponse.json(article);
  } catch {
    return NextResponse.json({ error: "Article not found" }, { status: 404 });
  }
}
```

Endpoint jest oznaczony jako `dynamic = "force-dynamic"`, co oznacza, że zawsze wykonuje się na żądanie i nie jest cache'owany.

### Strony aplikacji

#### Strona główna miejsca

Strona `/places/[placeId]` wyświetla informacje o miejscu i wszystkie dostępne warianty artykułów:

```17:148:app/places/[placeId]/page.tsx
export default function PlacePage({ params }: PlacePageProps) {
  const [place, setPlace] = useState<Place | null>(null);
  const [articles, setArticles] = useState<{
    adult_full: Article | null;
    adult_short: Article | null;
    child_short: Article | null;
  } | null>(null);
  const [placeId, setPlaceId] = useState<string>("");

  useEffect(() => {
    async function loadData() {
      const resolvedParams = await params;
      setPlaceId(resolvedParams.placeId);
      const placeData = await getPlace(resolvedParams.placeId);
      if (!placeData) {
        notFound();
        return;
      }
      setPlace(placeData);
      const articlesData = await getAllArticlesForPlace(resolvedParams.placeId);
      setArticles(articlesData);
    }
    loadData();
  }, [params]);

  if (!place || !articles) {
    return null;
  }

  const articleConfigs = [
    { key: "adult_full", label: "Dorośli – pełny", icon: "1", article: articles.adult_full },
    { key: "adult_short", label: "Dorośli – skrót", icon: "2", article: articles.adult_short },
    { key: "child_short", label: "Dzieci – skrót", icon: "3", article: articles.child_short },
  ];

  return (
    <main className="container mx-auto px-4 py-16 max-w-4xl">
      {/* Back link */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Link 
          href="/" 
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-8 transition-colors"
        >
          ← Powrót
        </Link>
      </motion.div>

      {/* Place header */}
      <motion.header
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="mb-12"
      >
        <div className="relative h-64 w-full rounded-md overflow-hidden bg-muted mb-6 shadow-md"> 
          <Image
            src={place.thumbnail}
            alt={place.name}
            fill
            className="object-cover"
            priority
          />
        </div>
        <h1 className="text-4xl font-medium mb-2">{place.name}</h1>
        <p className="text-muted-foreground text-sm">{place.description}</p>
      </motion.header>

      {/* Articles section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="mb-12"
      >
        <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground mb-6">
          Wersje przewodnika
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {articleConfigs.map((config, index) =>
            config.article ? (
              <ArticleCard
                key={config.key}
                article={config.article}
                label={config.label}
                icon={config.icon}
                index={index}
              />
            ) : (
              <motion.div
                key={config.key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="rounded-md border border-dashed border-border p-4 text-center text-muted-foreground text-sm shadow-sm"
              >
                {config.label}
                <br />
                <span className="text-xs">Niedostępny</span>
              </motion.div>
            )
          )}
        </div>
      </motion.section>

      {/* Compare section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="border-t border-border pt-8"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-medium mb-1">Porównaj wersje</h2>
            <p className="text-sm text-muted-foreground">
              Zobacz wszystkie wersje obok siebie
            </p>
          </div>
          <Link href={`/places/compare/${placeId}`}>
            <Button variant="outline" size="sm" className="shadow-sm hover:shadow-md transition-shadow">
              Porównaj
            </Button>
          </Link>
        </div>
      </motion.section>
    </main>
  );
}
```

Strona wykorzystuje React hooks (`useState`, `useEffect`) do zarządzania stanem i pobierania danych. Dane są pobierane asynchronicznie przy montowaniu komponentu.

#### Strona pojedynczego artykułu

Strona `/places/[placeId]/[style]` wyświetla pełną treść artykułu w wybranym stylu. Strona zawiera również formularz do oceny artykułu.

### Komponenty UI

Aplikacja wykorzystuje komponenty z biblioteki Radix UI oraz własne komponenty:

- **ArticleCard**: Karta prezentująca wariant artykułu
- **ArticleTabs**: Zakładki do przełączania między wariantami
- **RatingSingleForm**: Formularz oceny pojedynczego artykułu
- **RatingCompareForm**: Formularz oceny porównawczej

Wszystkie komponenty wykorzystują Tailwind CSS do stylizacji oraz Framer Motion do animacji.

### Zarządzanie danymi

Moduł `lib/data.ts` zawiera funkcje pomocnicze do pobierania danych z API:

```15:34:lib/data.ts
export async function getArticle(
  placeId: string,
  style: string
): Promise<Article | null> {
  const res = await fetch(`/api/articles/${placeId}/${style}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export async function getAllArticlesForPlace(
  placeId: string
): Promise<{ adult_full: Article | null; adult_short: Article | null; child_short: Article | null }> {
  const [adult_full, adult_short, child_short] = await Promise.all([
    getArticle(placeId, "adult_full"),
    getArticle(placeId, "adult_short"),
    getArticle(placeId, "child_short"),
  ]);

  return { adult_full, adult_short, child_short };
}
```

Funkcje wykorzystują `fetch` z opcją `cache: "no-store"`, aby zawsze pobierać najnowsze dane.

## 3.5 Zbieranie opinii użytkowników

System zbiera opinie użytkowników na dwa sposoby: oceny pojedynczych artykułów oraz oceny porównawcze wszystkich wariantów dla danego miejsca.

### Oceny pojedynczych artykułów

Użytkownicy mogą ocenić pojedynczy artykuł za pomocą formularza `RatingSingleForm`, który pojawia się na stronie artykułu.

#### Struktura danych oceny

Ocena pojedynczego artykułu zawiera następujące pola:

```17:29:lib/types.ts
export interface SingleRating {
  id: string;
  placeId: string;
  articleStyle: string;
  timestamp: string;
  clarity: number;
  styleMatch: number;
  structure: number;
  usefulness: number;
  length: "too_short" | "just_right" | "too_long";
  enjoyment: number;
  comment?: string;
}
```

- **clarity**: Ocena jasności artykułu (1-5)
- **styleMatch**: Ocena dopasowania stylu do grupy docelowej (1-5)
- **structure**: Ocena struktury artykułu (1-5)
- **usefulness**: Ocena użyteczności (1-5)
- **length**: Ocena długości artykułu (too_short, just_right, too_long)
- **enjoyment**: Ocena przyjemności czytania (1-5)
- **comment**: Opcjonalny komentarz tekstowy

#### Endpoint API

Endpoint `/api/rate-single` obsługuje zapisywanie ocen:

```7:50:app/api/rate-single/route.ts
export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Create rating object
    const rating = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      placeId: body.placeId,
      articleStyle: body.articleStyle,
      clarity: parseInt(body.clarity) || 0,
      styleMatch: parseInt(body.styleMatch) || 0,
      structure: parseInt(body.structure) || 0,
      usefulness: parseInt(body.usefulness) || 0,
      length: body.length || "",
      enjoyment: parseInt(body.enjoyment) || 0,
      comment: body.comment || "",
    };

    // Read existing ratings
    let ratings = [];
    try {
      const data = await fs.readFile(RATINGS_FILE, "utf-8");
      ratings = JSON.parse(data);
    } catch {
      // File doesn't exist or is empty, start with empty array
      ratings = [];
    }

    // Add new rating
    ratings.push(rating);

    // Write back to file
    await fs.writeFile(RATINGS_FILE, JSON.stringify(ratings, null, 2), "utf-8");

    return NextResponse.json({ success: true, id: rating.id });
  } catch (error) {
    console.error("Error saving rating:", error);
    return NextResponse.json(
      { success: false, error: "Failed to save rating" },
      { status: 500 }
    );
  }
}
```

Oceny są zapisywane w pliku `data/ratings/single.json` jako tablica obiektów. Każda ocena otrzymuje unikalny identyfikator UUID i timestamp.

#### Formularz oceny

Komponent `RatingSingleForm` wyświetla formularz z polami do oceny:

```67:108:components/RatingSingleForm.tsx
export function RatingSingleForm({
  placeId,
  articleStyle,
  onSuccess,
}: RatingSingleFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    clarity: "",
    styleMatch: "",
    structure: "",
    usefulness: "",
    length: "",
    enjoyment: "",
    comment: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/rate-single", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          placeId,
          articleStyle,
          ...formData,
        }),
      });

      if (response.ok) {
        setSubmitted(true);
        onSuccess?.();
      }
    } catch (error) {
      console.error("Error submitting rating:", error);
    } finally {
      setIsSubmitting(false);
    }
  };
```

Formularz wykorzystuje komponenty Radix UI (RadioGroup) do wyboru ocen na skali 1-5 oraz pole tekstowe do komentarza.

### Oceny porównawcze

Użytkownicy mogą również wypełnić ankietę porównawczą, która pozwala ocenić wszystkie trzy warianty artykułów jednocześnie. Ankieta jest dostępna na stronie `/places/compare/[placeId]`.

#### Struktura danych oceny porównawczej

Ocena porównawcza zawiera następujące pola:

```31:41:lib/types.ts
export interface CompareRating {
  id: string;
  placeId: string;
  timestamp: string;
  bestOverall: string;
  easiestToUnderstand: string;
  bestForChildren: string;
  bestForQuickLook: string;
  bestForPlanning: string;
  comment?: string;
}
```

Każde pole (oprócz `comment`) zawiera identyfikator stylu (`adult_full`, `adult_short`, `child_short`), który użytkownik wybrał jako najlepszy w danej kategorii.

#### Endpoint API

Endpoint `/api/rate-compare` obsługuje zapisywanie ocen porównawczych:

```7:48:app/api/rate-compare/route.ts
export async function POST(request: Request) {
  try {
    const body = await request.json();

    // Create rating object
    const rating = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      placeId: body.placeId,
      bestOverall: body.bestOverall || "",
      easiestToUnderstand: body.easiestToUnderstand || "",
      bestForChildren: body.bestForChildren || "",
      bestForQuickLook: body.bestForQuickLook || "",
      bestForPlanning: body.bestForPlanning || "",
      comment: body.comment || "",
    };

    // Read existing ratings
    let ratings = [];
    try {
      const data = await fs.readFile(RATINGS_FILE, "utf-8");
      ratings = JSON.parse(data);
    } catch {
      // File doesn't exist or is empty, start with empty array
      ratings = [];
    }

    // Add new rating
    ratings.push(rating);

    // Write back to file
    await fs.writeFile(RATINGS_FILE, JSON.stringify(ratings, null, 2), "utf-8");

    return NextResponse.json({ success: true, id: rating.id });
  } catch (error) {
    console.error("Error saving comparison:", error);
    return NextResponse.json(
      { success: false, error: "Failed to save comparison" },
      { status: 500 }
    );
  }
}
```

Oceny porównawcze są zapisywane w pliku `data/ratings/compare.json`.

#### Formularz porównawczy

Komponent `RatingCompareForm` wyświetla formularz z pytaniami porównawczymi:

```63:98:components/RatingCompareForm.tsx
export function RatingCompareForm({ placeId, onSuccess }: RatingCompareFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    bestOverall: "",
    easiestToUnderstand: "",
    bestForChildren: "",
    bestForQuickLook: "",
    bestForPlanning: "",
    comment: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/rate-compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          placeId,
          ...formData,
        }),
      });

      if (response.ok) {
        setSubmitted(true);
        onSuccess?.();
      }
    } catch (error) {
      console.error("Error submitting comparison:", error);
    } finally {
      setIsSubmitting(false);
    }
  };
```

Formularz pozwala użytkownikowi wybrać najlepszy wariant dla każdej kategorii z listy rozwijanej.

### Przechowywanie danych

Wszystkie oceny są przechowywane w plikach JSON w katalogu `data/ratings/`:
- `single.json` - oceny pojedynczych artykułów
- `compare.json` - oceny porównawcze

Pliki są odczytywane i zapisywane synchronicznie przy użyciu Node.js `fs` API. W przypadku braku pliku, system tworzy pustą tablicę.

### Wykorzystanie danych

Zebrane oceny mogą być wykorzystane do:
- Analizy jakości generowanych artykułów
- Porównania skuteczności różnych wariantów
- Identyfikacji obszarów wymagających poprawy
- Badania preferencji użytkowników

Dane są dostępne w formacie JSON i mogą być łatwo przetwarzane przez narzędzia analityczne lub skrypty Python (np. w katalogu `analytics/`).





