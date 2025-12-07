"""
paragraph_count.py - Liczba akapitów

OPIS METRYKI:
Zlicza liczbę akapitów w tekście.
Akapit definiowany jako blok tekstu oddzielony pustymi liniami.

INTERPRETACJA:
- Więcej akapitów = lepiej podzielony tekst
- Mniej akapitów = bardziej zwarty tekst
- Stosunek akapitów do zdań pokazuje strukturę tekstu

ZASTOSOWANIE:
- Ocena struktury tekstu
- Porównanie organizacji treści między wersjami
"""

from common import (
    process_articles_parallel,
    save_aggregated_metric,
)


def calculate_paragraph_count(text: str) -> int:
    """
    Oblicza liczbę akapitów w tekście.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Liczba akapitów
    """
    # Podziel po podwójnych newline (lub więcej)
    paragraphs = text.split("\n\n")
    
    # Filtruj puste i te zawierające tylko whitespace
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    return len(paragraphs)


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="paragraph_count",
        calculate_func=calculate_paragraph_count
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("paragraph_count", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

