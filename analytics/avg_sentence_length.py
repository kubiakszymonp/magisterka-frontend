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
    process_articles_parallel,
    save_aggregated_metric,
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


def get_extra_data(content: str) -> dict:
    """Zwraca dodatkowe dane dla avg_sentence_length."""
    tokens = get_tokens(content)
    sentences = get_sentences(content)
    return {
        "word_count": len(tokens),
        "sentence_count": len(sentences)
    }


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="avg_sentence_length",
        calculate_func=calculate_avg_sentence_length,
        extra_data_func=get_extra_data
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("avg_sentence_length", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

