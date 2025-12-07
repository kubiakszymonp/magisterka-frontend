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
    list_articles,
    load_article,
    save_metric_result,
    VERSIONS,
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
    articles = list_articles()
    
    print(f"Przetwarzanie {len(articles)} artykułów...")
    
    for article_name in articles:
        for version in VERSIONS:
            try:
                data = load_article(article_name, version)
                content = data.get("content", "")
                
                paragraph_count = calculate_paragraph_count(content)
                
                save_metric_result(
                    metric_name="paragraph_count",
                    article_name=article_name,
                    version=version,
                    value=paragraph_count
                )
                
                print(f"  {article_name}/{version}: {paragraph_count} akapitów")
                
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

