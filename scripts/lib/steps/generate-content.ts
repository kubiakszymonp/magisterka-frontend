import type { ChainContext } from "../types";
import { getAgeTargetDescription, getVolumeDescription, buildSourcesPrompt } from "../prompts";

export const STEP_NAME = "generate_content";
export const TEMPERATURE = 0.1;

export function buildPrompt(ctx: ChainContext, outline: string): { system: string; user: string } {
  const age = getAgeTargetDescription(ctx);
  const volume = getVolumeDescription(ctx);

  const system = `Jesteś ekspertem przewodnikiem turystycznym. Twoją rolą jest stworzenie szczegółowych opisów dla każdego punktu z konspektu.

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name} - ${age.prompt}
- Czas: ${volume.name} - ${volume.prompt}

INSTRUKCJE:
- Rozwiń każdy punkt z konspektu w szczegółowy opis
- Dostosuj objętość do kategorii czasowej, ale staraj się rozpoczęte wątki kończyć w sposób pełny, nie pozostawiając niedomówień
- Bazuj na źródłach, ale twórz płynny tekst
- Zachowaj merytoryczność i dokładność
- Jeżeli pojawiają się jakieś nawiązania kulturowe albo do postaci, to je krótko opisz, żeby czytelnik złapał kontekst
- Artykuł ma być informatywny i kompletny, żeby nikt nie musiał się później zastanawiać o co chodzi
- NIE UŻYWAJ FORMATOWANIA MARKDOWN - tylko czysty tekst`;

  const user = `Miejsce: ${ctx.placeName}

KATEGORIE DOCELOWE:
- Grupa wiekowa: ${age.name}
- Czas: ${volume.name}

ŹRÓDŁA INFORMACJI:
${buildSourcesPrompt(ctx.sourceArticles)}

Konspekt do rozwinięcia:
${outline}

Stwórz szczegółowe opisy dla każdego punktu:`;

  return { system, user };
}

