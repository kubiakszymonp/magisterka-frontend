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
    process_articles_parallel,
    save_aggregated_metric,
)


def calculate_avg_word_length_full(text: str) -> dict:
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


def calculate_avg_word_length(text: str) -> float:
    """Zwraca tylko średnią długość słowa."""
    results = calculate_avg_word_length_full(text)
    return results["avg_word_length"]


def get_extra_data_avg_word_length(content: str) -> dict:
    """Zwraca dodatkowe dane dla avg_word_length."""
    results = calculate_avg_word_length_full(content)
    return {
        "total_chars": results["total_chars"],
        "word_count": results["word_count"]
    }


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="avg_word_length",
        calculate_func=calculate_avg_word_length,
        extra_data_func=get_extra_data_avg_word_length
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("avg_word_length", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

