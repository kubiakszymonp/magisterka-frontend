"""
jaccard_similarity.py - Podobieństwo Jaccarda między wersjami artykułu

OPIS METRYKI:
Indeks Jaccarda mierzy podobieństwo między dwoma zbiorami słów.
Oblicza stosunek części wspólnej do sumy zbiorów.

WZÓR:
J(A, B) = |A ∩ B| / |A ∪ B|

INTERPRETACJA:
- Wartość od 0 do 1
- 0 = brak wspólnych słów
- 1 = identyczne zbiory słów
- Typowe wartości między wersjami: 0.3-0.7

PORÓWNANIA:
- adult_full vs adult_short
- adult_full vs child_short  
- adult_short vs child_short

ZASTOSOWANIE:
- Ocena jak bardzo różnią się wersje artykułu pod względem użytego słownictwa
- Sprawdzenie czy wersja dla dzieci używa podobnego słownictwa co dorosła
"""

from itertools import combinations

from common import (
    get_lemmas,
    list_articles,
    load_article,
    save_aggregated_comparison_metric,
    save_comparison_result,
    VERSIONS,
)


def calculate_jaccard(set_a: set, set_b: set) -> float:
    """
    Oblicza indeks Jaccarda między dwoma zbiorami.
    
    Args:
        set_a: Pierwszy zbiór
        set_b: Drugi zbiór
    
    Returns:
        Indeks Jaccarda (0-1)
    """
    if len(set_a) == 0 and len(set_b) == 0:
        return 1.0
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    if union == 0:
        return 0.0
    
    return round(intersection / union, 4)


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    articles = list_articles()
    
    print(f"Przetwarzanie {len(articles)} artykułów...")
    
    # Pary do porównania
    version_pairs = list(combinations(VERSIONS, 2))
    
    aggregated = {}
    
    for article_name in articles:
        # Wczytaj wszystkie wersje
        version_lemmas = {}
        
        for version in VERSIONS:
            try:
                data = load_article(article_name, version)
                content = data.get("content", "")
                lemmas = set(get_lemmas(content, lowercase=True))
                version_lemmas[version] = lemmas
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
        
        # Oblicz podobieństwo dla każdej pary
        comparisons = {}
        
        for v1, v2 in version_pairs:
            if v1 in version_lemmas and v2 in version_lemmas:
                jaccard = calculate_jaccard(version_lemmas[v1], version_lemmas[v2])
                key = f"{v1}__{v2}"
                comparisons[key] = jaccard
        
        if comparisons:
            save_comparison_result(
                metric_name="jaccard_similarity",
                article_name=article_name,
                comparisons=comparisons
            )
            
            aggregated[article_name] = comparisons
            
            print(f"  {article_name}:")
            for key, val in comparisons.items():
                print(f"    {key}: {val}")
    
    # Zapisz agregowany JSON
    if aggregated:
        save_aggregated_comparison_metric("jaccard_similarity", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

