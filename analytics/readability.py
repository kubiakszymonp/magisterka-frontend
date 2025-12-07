"""
readability.py - Wskaźniki czytelności (Flesch Reading Ease, Fog Index)

OPIS METRYK:

1. FLESCH READING EASE (FRE)
   Mierzy łatwość czytania tekstu na skali 0-100.
   
   WZÓR (adaptowany dla polskiego):
   FRE = 206.835 - (1.015 × ASL) - (84.6 × ASW)
   gdzie:
   - ASL = średnia długość zdania (w słowach)
   - ASW = średnia liczba sylab na słowo
   
   INTERPRETACJA:
   - 90-100: Bardzo łatwy (dla 11-latków)
   - 80-89: Łatwy
   - 70-79: Dość łatwy
   - 60-69: Standardowy
   - 50-59: Dość trudny
   - 30-49: Trudny
   - 0-29: Bardzo trudny (akademicki)

2. GUNNING FOG INDEX
   Szacuje liczbę lat edukacji potrzebnych do zrozumienia tekstu.
   
   WZÓR:
   FOG = 0.4 × (ASL + PHW)
   gdzie:
   - ASL = średnia długość zdania
   - PHW = procent "trudnych słów" (3+ sylaby)
   
   INTERPRETACJA:
   - 6: Bardzo łatwy (szkoła podstawowa)
   - 8-10: Łatwy (gimnazjum)
   - 10-12: Średni (liceum)
   - 12-14: Trudny (studia)
   - 14+: Bardzo trudny (specjalistyczny)

UWAGA:
Wzory zostały stworzone dla języka angielskiego. Dla polskiego wyniki
mogą być przesunięte ze względu na różnice w morfologii (polski ma
więcej sylab na słowo). Wartości są porównywalne między tekstami
polskimi, ale nie bezpośrednio z angielskimi benchmarkami.

ZASTOSOWANIE:
- Ocena dostosowania tekstu do grupy docelowej (adult vs child)
- Porównanie czytelności różnych wersji artykułów
"""

from common import (
    get_tokens,
    get_sentences,
    count_syllables_polish,
    process_articles_parallel,
    save_aggregated_metric,
)


def calculate_flesch_reading_ease(text: str) -> float:
    """
    Oblicza Flesch Reading Ease dla tekstu polskiego.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Wynik FRE (wyższy = łatwiejszy tekst)
    """
    tokens = get_tokens(text)
    sentences = get_sentences(text)
    
    if len(sentences) == 0 or len(tokens) == 0:
        return 0.0
    
    # Średnia długość zdania
    asl = len(tokens) / len(sentences)
    
    # Średnia liczba sylab na słowo
    total_syllables = sum(count_syllables_polish(word) for word in tokens)
    asw = total_syllables / len(tokens)
    
    # Wzór Flesch Reading Ease
    fre = 206.835 - (1.015 * asl) - (84.6 * asw)
    
    return round(fre, 2)


def calculate_fog_index(text: str) -> float:
    """
    Oblicza Gunning Fog Index dla tekstu.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Wynik Fog Index (liczba lat edukacji)
    """
    tokens = get_tokens(text)
    sentences = get_sentences(text)
    
    if len(sentences) == 0 or len(tokens) == 0:
        return 0.0
    
    # Średnia długość zdania
    asl = len(tokens) / len(sentences)
    
    # Procent trudnych słów (3+ sylaby)
    hard_words = [word for word in tokens if count_syllables_polish(word) >= 3]
    phw = (len(hard_words) / len(tokens)) * 100
    
    # Wzór Gunning Fog Index
    fog = 0.4 * (asl + phw)
    
    return round(fog, 2)


def get_readability_level(fre: float) -> str:
    """Zwraca opis poziomu czytelności na podstawie FRE."""
    if fre >= 90:
        return "bardzo_łatwy"
    elif fre >= 80:
        return "łatwy"
    elif fre >= 70:
        return "dość_łatwy"
    elif fre >= 60:
        return "standardowy"
    elif fre >= 50:
        return "dość_trudny"
    elif fre >= 30:
        return "trudny"
    else:
        return "bardzo_trudny"


def calculate_readability(text: str) -> dict:
    """Oblicza wskaźniki czytelności i zwraca główną wartość."""
    fre = calculate_flesch_reading_ease(text)
    fog = calculate_fog_index(text)
    
    return {
        "flesch_reading_ease": fre,
        "fog_index": fog,
        "readability_level": get_readability_level(fre)
    }


def get_extra_data_readability(content: str) -> dict:
    """Zwraca dodatkowe dane dla readability."""
    tokens = get_tokens(content)
    sentences = get_sentences(content)
    total_syllables = sum(count_syllables_polish(w) for w in tokens)
    hard_words = [w for w in tokens if count_syllables_polish(w) >= 3]
    
    return {
        "avg_sentence_length": round(len(tokens) / max(len(sentences), 1), 2),
        "avg_syllables_per_word": round(total_syllables / max(len(tokens), 1), 2),
        "hard_words_count": len(hard_words),
        "hard_words_percent": round(len(hard_words) / max(len(tokens), 1) * 100, 2)
    }


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="readability",
        calculate_func=calculate_readability,
        extra_data_func=get_extra_data_readability
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("readability", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

