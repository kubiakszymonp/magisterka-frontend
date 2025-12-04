import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription, buildSourcesPrompt } from "../prompts";

export const STEP_NAME = "generate_content";

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

