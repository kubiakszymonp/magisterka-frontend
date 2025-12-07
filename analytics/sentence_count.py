"""
sentence_count.py - Liczba zdań w tekście

OPIS METRYKI:
Liczba zdań (Sentence Count) zlicza wszystkie zdania w tekście.
Wykorzystuje tokenizator zdań z biblioteki spaCy, który rozpoznaje
końcówki zdań (kropki, pytajniki, wykrzykniki) oraz kontekst.

INTERPRETACJA:
- Wyższa wartość = więcej zdań w tekście
- W połączeniu z liczbą słów pozwala obliczyć średnią długość zdania
- Teksty dla dzieci powinny mieć więcej krótszych zdań

ZASTOSOWANIE:
- Analiza struktury tekstu
- Obliczanie średniej długości zdania
- Porównanie złożoności składniowej między wersjami
"""

from common import (
    get_sentences,
    process_articles_parallel,
    save_aggregated_metric,
)


def calculate_sentence_count(text: str) -> int:
    """
    Oblicza liczbę zdań w tekście.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Liczba zdań
    """
    sentences = get_sentences(text)
    return len(sentences)


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="sentence_count",
        calculate_func=calculate_sentence_count
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("sentence_count", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

