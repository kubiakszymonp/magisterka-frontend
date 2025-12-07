"""
mtld.py - Measure of Textual Lexical Diversity (MTLD)

OPIS METRYKI:
MTLD (Measure of Textual Lexical Diversity) to zaawansowana miara
różnorodności leksykalnej, która jest odporna na długość tekstu
(w przeciwieństwie do TTR).

ALGORYTM:
1. Przechodzi przez tekst słowo po słowie
2. Oblicza TTR dla narastającego fragmentu
3. Gdy TTR spada poniżej progu (domyślnie 0.72), kończy "faktor"
4. Zlicza liczbę faktorów i oblicza średnią ich długość
5. Powtarza proces od końca tekstu (bi-directional)
6. Końcowy MTLD to średnia z obu kierunków

INTERPRETACJA:
- Wyższa wartość = większa różnorodność leksykalna
- Typowe wartości: 50-150
- < 50: niskie zróżnicowanie słownictwa
- 50-100: umiarkowane zróżnicowanie
- > 100: wysokie zróżnicowanie słownictwa

ZALETY NAD TTR:
- Nie zależy od długości tekstu
- Można porównywać teksty o różnej długości
- Bardziej stabilna miara

ZASTOSOWANIE:
- Ocena bogactwa słownictwa generowanych tekstów
- Porównanie różnorodności między wersjami artykułów
- Analiza czy teksty dla dzieci mają prostsze słownictwo
"""

from lexical_diversity import lex_div as ld

from common import (
    get_tokens,
    get_lemmas,
    list_articles,
    load_article,
    save_aggregated_metric,
    save_metric_result,
    VERSIONS,
)


def calculate_mtld(tokens: list[str]) -> float:
    """
    Oblicza MTLD dla listy tokenów.
    
    Args:
        tokens: Lista tokenów (słów)
    
    Returns:
        Wartość MTLD
    """
    if len(tokens) < 50:
        # MTLD potrzebuje minimum ~50 tokenów dla sensownych wyników
        return 0.0
    
    try:
        mtld_value = ld.mtld(tokens)
        return round(mtld_value, 2)
    except Exception:
        return 0.0


def calculate_mtld_from_text(text: str) -> dict:
    """
    Oblicza MTLD dla tekstu - zarówno na tokenach jak i lematach.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Słownik z MTLD na tokenach i lematach
    """
    tokens = get_tokens(text, lowercase=True)
    lemmas = get_lemmas(text, lowercase=True)
    
    return {
        "mtld_tokens": calculate_mtld(tokens),
        "mtld_lemmas": calculate_mtld(lemmas),
        "token_count": len(tokens),
        "lemma_count": len(lemmas)
    }


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    articles = list_articles()
    
    print(f"Przetwarzanie {len(articles)} artykułów...")
    
    aggregated = {}
    
    for article_name in articles:
        aggregated[article_name] = {}
        
        for version in VERSIONS:
            try:
                data = load_article(article_name, version)
                content = data.get("content", "")
                
                results = calculate_mtld_from_text(content)
                
                value = {
                    "mtld_tokens": results["mtld_tokens"],
                    "mtld_lemmas": results["mtld_lemmas"]
                }
                
                save_metric_result(
                    metric_name="mtld",
                    article_name=article_name,
                    version=version,
                    value=value,
                    extra_data={
                        "token_count": results["token_count"],
                        "lemma_count": results["lemma_count"]
                    }
                )
                
                aggregated[article_name][version] = value
                
                print(f"  {article_name}/{version}: MTLD(tokens)={results['mtld_tokens']}, MTLD(lemmas)={results['mtld_lemmas']}")
                
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
    
    # Zapisz agregowany JSON
    save_aggregated_metric("mtld", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

