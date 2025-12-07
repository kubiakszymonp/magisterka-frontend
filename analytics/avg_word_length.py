"""
avg_word_length.py - Średnia długość słowa

OPIS METRYKI:
Średnia długość słowa (Average Word Length) mierzy przeciętną
liczbę znaków w słowach tekstu.

WZÓR:
AWL = suma_długości_słów / liczba_słów

INTERPRETACJA:
- Wyższa wartość = dłuższe, bardziej złożone słowa
- Niższa wartość = krótsze, prostsze słowa
- Typowe wartości dla polskiego: 5-7 znaków
- Teksty dla dzieci powinny mieć niższą wartość

ZASTOSOWANIE:
- Ocena złożoności słownictwa
- Porównanie między wersjami (adult vs child)
- Uzupełnienie metryki rzadkich słów
"""

from common import (
    get_tokens,
    list_articles,
    load_article,
    save_aggregated_metric,
    save_metric_result,
    VERSIONS,
)


def calculate_avg_word_length(text: str) -> dict:
    """
    Oblicza średnią długość słowa.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Słownik ze średnią i statystykami
    """
    tokens = get_tokens(text, lowercase=False)
    
    if len(tokens) == 0:
        return {
            "avg_word_length": 0.0,
            "total_chars": 0,
            "word_count": 0
        }
    
    total_chars = sum(len(word) for word in tokens)
    avg_length = total_chars / len(tokens)
    
    return {
        "avg_word_length": round(avg_length, 2),
        "total_chars": total_chars,
        "word_count": len(tokens)
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
                
                results = calculate_avg_word_length(content)
                
                save_metric_result(
                    metric_name="avg_word_length",
                    article_name=article_name,
                    version=version,
                    value=results["avg_word_length"],
                    extra_data={
                        "total_chars": results["total_chars"],
                        "word_count": results["word_count"]
                    }
                )
                
                aggregated[article_name][version] = results["avg_word_length"]
                
                print(f"  {article_name}/{version}: {results['avg_word_length']} znaków/słowo")
                
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
    
    # Zapisz agregowany JSON
    save_aggregated_metric("avg_word_length", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

