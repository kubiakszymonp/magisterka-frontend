"""
word_count.py - Liczba słów w tekście

OPIS METRYKI:
Liczba słów (Word Count) to podstawowa metryka ilościowa tekstu.
Zlicza wszystkie tokeny alfabetyczne w tekście (pomija cyfry, interpunkcję, symbole).

INTERPRETACJA:
- Wyższa wartość = dłuższy tekst
- Pozwala porównać objętość różnych wersji artykułów (full vs short)
- Bazowa metryka do obliczania innych wskaźników (np. średnia długość zdania)

ZASTOSOWANIE:
- Porównanie długości wersji artykułów (adult_full vs adult_short vs child_short)
- Analiza czy generator przestrzega limitów długości
"""

from common import (
    get_tokens,
    list_articles,
    load_article,
    save_aggregated_metric,
    save_metric_result,
    VERSIONS,
)


def calculate_word_count(text: str) -> int:
    """
    Oblicza liczbę słów w tekście.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Liczba słów (tokenów alfabetycznych)
    """
    tokens = get_tokens(text)
    return len(tokens)


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
                
                word_count = calculate_word_count(content)
                
                save_metric_result(
                    metric_name="word_count",
                    article_name=article_name,
                    version=version,
                    value=word_count
                )
                
                aggregated[article_name][version] = word_count
                
                print(f"  {article_name}/{version}: {word_count} słów")
                
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
    
    # Zapisz agregowany JSON
    save_aggregated_metric("word_count", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

