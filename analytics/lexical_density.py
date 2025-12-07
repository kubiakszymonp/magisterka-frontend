"""
lexical_density.py - Gęstość leksykalna

OPIS METRYKI:
Gęstość leksykalna (Lexical Density) mierzy proporcję słów treściowych
(content words) do wszystkich słów w tekście.

SŁOWA TREŚCIOWE (content words):
- Rzeczowniki (NOUN)
- Czasowniki (VERB)
- Przymiotniki (ADJ)
- Przysłówki (ADV)

SŁOWA FUNKCYJNE (function words):
- Przyimki, spójniki, zaimki, rodzajniki, partykuły, etc.
- Pełnią rolę gramatyczną, nie niosą głównego znaczenia

WZÓR:
Lexical Density = liczba_słów_treściowych / liczba_wszystkich_słów × 100%

INTERPRETACJA:
- Wyższa wartość (50-70%) = tekst gęsty informacyjnie
- Niższa wartość (40-50%) = tekst bardziej konwersacyjny/potoczny
- Teksty pisane: 40-65%
- Teksty mówione: 35-50%
- Teksty naukowe: 55-70%

ZASTOSOWANIE:
- Ocena "gęstości informacyjnej" tekstu
- Porównanie stylu między wersjami (adult vs child)
- Teksty dla dzieci mogą mieć niższą gęstość (więcej słów funkcyjnych)
"""

from common import (
    get_nlp,
    get_tokens,
    process_articles_parallel,
    save_aggregated_metric,
)


def calculate_lexical_density(text: str) -> dict:
    """
    Oblicza gęstość leksykalną tekstu.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Słownik z gęstością i statystykami
    """
    nlp = get_nlp()
    doc = nlp(text)
    
    # POS tags dla słów treściowych
    content_pos = {"NOUN", "VERB", "ADJ", "ADV"}
    
    # Zlicz tylko tokeny alfabetyczne
    all_words = [token for token in doc if token.is_alpha]
    content_words = [token for token in all_words if token.pos_ in content_pos]
    
    total_count = len(all_words)
    content_count = len(content_words)
    
    if total_count == 0:
        density = 0.0
    else:
        density = (content_count / total_count) * 100
    
    # Zlicz poszczególne kategorie
    pos_counts = {}
    for token in all_words:
        pos = token.pos_
        pos_counts[pos] = pos_counts.get(pos, 0) + 1
    
    return {
        "lexical_density": round(density, 2),
        "content_words_count": content_count,
        "total_words_count": total_count,
        "function_words_count": total_count - content_count,
        "pos_breakdown": {
            "nouns": pos_counts.get("NOUN", 0),
            "verbs": pos_counts.get("VERB", 0),
            "adjectives": pos_counts.get("ADJ", 0),
            "adverbs": pos_counts.get("ADV", 0)
        }
    }


def get_density_interpretation(density: float) -> str:
    """Zwraca interpretację gęstości leksykalnej."""
    if density >= 60:
        return "bardzo_gęsty"
    elif density >= 50:
        return "gęsty"
    elif density >= 40:
        return "umiarkowany"
    else:
        return "niski"


def calculate_lexical_density_value(text: str) -> float:
    """Zwraca tylko wartość gęstości leksykalnej."""
    results = calculate_lexical_density(text)
    return results["lexical_density"]


def get_extra_data_lexical_density(content: str) -> dict:
    """Zwraca dodatkowe dane dla lexical_density."""
    results = calculate_lexical_density(content)
    return {
        "content_words_count": results["content_words_count"],
        "total_words_count": results["total_words_count"],
        "function_words_count": results["function_words_count"],
        "pos_breakdown": results["pos_breakdown"],
        "interpretation": get_density_interpretation(results["lexical_density"])
    }


def format_lexical_density_output(value: float) -> str:
    """Formatuje wartość lexical_density do wyświetlenia."""
    return f"{value}% ({get_density_interpretation(value)})"


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_articles_parallel(
        metric_name="lexical_density",
        calculate_func=calculate_lexical_density_value,
        extra_data_func=get_extra_data_lexical_density
    )
    
    # Zapisz agregowany JSON
    save_aggregated_metric("lexical_density", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

