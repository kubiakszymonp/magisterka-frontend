"""
avg_sentence_length.py - Średnia długość zdania

OPIS METRYKI:
Średnia długość zdania (Average Sentence Length - ASL) to stosunek
liczby słów do liczby zdań w tekście.

WZÓR:
ASL = liczba_słów / liczba_zdań

INTERPRETACJA:
- Niższa wartość (10-15 słów) = prostszy tekst, łatwiejszy w odbiorze
- Wyższa wartość (20+ słów) = bardziej złożony tekst, trudniejszy w odbiorze
- Teksty dla dzieci powinny mieć niższą ASL
- Teksty naukowe/formalne mają wyższą ASL

ZASTOSOWANIE:
- Ocena czytelności tekstu
- Porównanie złożoności składniowej między wersjami (adult vs child)
- Analiza stylu pisania generatora
"""

from common import (
    get_tokens,
    get_sentences,
    list_articles,
    load_article,
    save_aggregated_metric,
    save_metric_result,
    VERSIONS,
)


def calculate_avg_sentence_length(text: str) -> float:
    """
    Oblicza średnią długość zdania w tekście.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Średnia liczba słów na zdanie (zaokrąglona do 2 miejsc)
    """
    tokens = get_tokens(text)
    sentences = get_sentences(text)
    
    if len(sentences) == 0:
        return 0.0
    
    avg_length = len(tokens) / len(sentences)
    return round(avg_length, 2)


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
                
                avg_length = calculate_avg_sentence_length(content)
                
                # Dodatkowe dane dla kontekstu
                tokens = get_tokens(content)
                sentences = get_sentences(content)
                
                save_metric_result(
                    metric_name="avg_sentence_length",
                    article_name=article_name,
                    version=version,
                    value=avg_length,
                    extra_data={
                        "word_count": len(tokens),
                        "sentence_count": len(sentences)
                    }
                )
                
                aggregated[article_name][version] = avg_length
                
                print(f"  {article_name}/{version}: {avg_length} słów/zdanie")
                
            except FileNotFoundError:
                print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
    
    # Zapisz agregowany JSON
    save_aggregated_metric("avg_sentence_length", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

