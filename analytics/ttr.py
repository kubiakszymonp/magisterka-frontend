"""
ttr.py - Type-Token Ratio (TTR)

OPIS METRYKI:
Type-Token Ratio (TTR) mierzy różnorodność leksykalną tekstu.
Jest to stosunek unikalnych słów (types) do wszystkich słów (tokens).

WZÓR:
TTR = liczba_unikalnych_słów / liczba_wszystkich_słów

INTERPRETACJA:
- Wartość od 0 do 1 (często wyrażana jako procent 0-100%)
- Wyższa wartość = większa różnorodność słownictwa
- Niższa wartość = więcej powtórzeń, bardziej ograniczone słownictwo
- Typowe wartości: 0.4-0.6 (40-60%)

OGRANICZENIA:
- TTR jest wrażliwy na długość tekstu - dłuższe teksty mają niższy TTR
  (bo słowa się powtarzają)
- Dlatego porównywanie TTR między tekstami o różnej długości jest problematyczne
- Dla dokładniejszej analizy użyj MTLD (mtld.py)

WARIANTY:
- TTR standardowy: na wszystkich tokenach
- TTR na lematach: na formach podstawowych słów (bardziej sprawiedliwy dla polskiego
  ze względu na bogatą odmianę)

ZASTOSOWANIE:
- Ocena bogactwa słownictwa generowanych tekstów
- Porównanie różnorodności leksykalnej między wersjami (uwaga na długość!)
"""

from common import (
    get_tokens,
    get_lemmas,
    process_articles_parallel,
    save_aggregated_metric,
)


def calculate_ttr(tokens: list[str]) -> float:
    """
    Oblicza Type-Token Ratio.
    
    Args:
        tokens: Lista tokenów (słów)
    
    Returns:
        TTR jako wartość 0-1
    """
    if len(tokens) == 0:
        return 0.0
    
    unique_tokens = set(tokens)
    ttr = len(unique_tokens) / len(tokens)
    
    return round(ttr, 4)


def calculate_ttr_from_text_full(text: str) -> dict:
    """
    Oblicza TTR dla tekstu - zarówno na tokenach jak i lematach.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Słownik z TTR na tokenach i lematach
    """
    tokens = get_tokens(text, lowercase=True)
    lemmas = get_lemmas(text, lowercase=True)
    
    return {
        "ttr_tokens": calculate_ttr(tokens),
        "ttr_lemmas": calculate_ttr(lemmas),
        "unique_tokens": len(set(tokens)),
        "total_tokens": len(tokens),
        "unique_lemmas": len(set(lemmas)),
        "total_lemmas": len(lemmas)
    }


def calculate_ttr_from_text(text: str) -> dict:
    """Zwraca główną wartość TTR (dict z ttr_tokens i ttr_lemmas)."""
    results = calculate_ttr_from_text_full(text)
    return {
        "ttr_tokens": results["ttr_tokens"],
        "ttr_lemmas": results["ttr_lemmas"]
    }


def get_extra_data_ttr(content: str) -> dict:
    """Zwraca dodatkowe dane dla TTR."""
    results = calculate_ttr_from_text_full(content)
    return {
        "unique_tokens": results["unique_tokens"],
        "total_tokens": results["total_tokens"],
        "unique_lemmas": results["unique_lemmas"],
        "total_lemmas": results["total_lemmas"]
    }


def format_ttr_output(value: dict) -> str:
    """Formatuje wartość TTR do wyświetlenia."""
    if isinstance(value, dict) and "ttr_tokens" in value:
        return f"TTR(tokens)={value['ttr_tokens']:.3f}, TTR(lemmas)={value['ttr_lemmas']:.3f}"
    return str(value)


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="ttr",
        calculate_func=calculate_ttr_from_text,
        extra_data_func=get_extra_data_ttr
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("ttr", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

