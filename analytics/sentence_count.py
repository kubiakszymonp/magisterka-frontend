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
    list_articles,
    load_article,
    save_aggregated_metric,
    save_metric_result,
    VERSIONS,
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
    articles = list_articles()
    
    print(f"Przetwarzanie {len(articles)} artykułów...")
    
    aggregated = {}
    
    for article_name in articles:
        aggregated[article_name] = {}
        
        for version in VERSIONS:
            try:
                data = load_article(article_name, version)
                content = data.get("content", "")
                
                sentence_count = calculate_sentence_count(content)
                
                save_metric_result(
                    metric_name="sentence_count",
                    article_name=article_name,
                    version=version,
                    value=sentence_count
                )
                
                aggregated[article_name][version] = sentence_count
                
                print(f"  {article_name}/{version}: {sentence_count} zdań")
                
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
    
    # Zapisz agregowany JSON
    save_aggregated_metric("sentence_count", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

