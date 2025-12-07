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
    process_articles_parallel,
    save_aggregated_metric,
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
    aggregated = process_articles_parallel(
        metric_name="word_count",
        calculate_func=calculate_word_count
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("word_count", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

