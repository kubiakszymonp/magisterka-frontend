"""
tfidf_overlap.py - Keyword overlap oparty na TF-IDF

OPIS METRYKI:
Mierzy podobieństwo między wersjami artykułu na podstawie
najważniejszych słów kluczowych (keywords) wyodrębnionych metodą TF-IDF.

METODA:
1. Dla każdej wersji oblicz TF-IDF
2. Wyodrębnij top N słów kluczowych (najwyższe TF-IDF)
3. Oblicz overlap między zbiorami keywords różnych wersji

TF-IDF (Term Frequency - Inverse Document Frequency):
- TF = częstość słowa w dokumencie
- IDF = log(liczba dokumentów / dokumenty zawierające słowo)
- TF-IDF = TF × IDF

INTERPRETACJA:
- Wyższa wartość = więcej wspólnych słów kluczowych
- Pokazuje czy wersje zachowują te same główne tematy/koncepty

ZASTOSOWANIE:
- Sprawdzenie czy różne wersje artykułu zachowują te same kluczowe pojęcia
- Analiza czy uproszczenie tekstu (child) nie traci ważnych słów kluczowych
"""

from itertools import combinations

from sklearn.feature_extraction.text import TfidfVectorizer

from common import (
    get_lemmas,
    load_article,
    process_comparison_articles_parallel,
    save_aggregated_comparison_metric,
    save_comparison_result,
    VERSIONS,
)

# Liczba top keywords do porównania
TOP_N_KEYWORDS = 20


def get_top_keywords(text: str, n: int = TOP_N_KEYWORDS) -> set[str]:
    """
    Wyodrębnia top N słów kluczowych z tekstu metodą TF-IDF.
    
    Args:
        text: Tekst do analizy
        n: Liczba top keywords
    
    Returns:
        Zbiór słów kluczowych
    """
    # Użyj lematów
    lemmas = get_lemmas(text, lowercase=True)
    
    if len(lemmas) < 5:
        return set(lemmas)
    
    # Przygotuj tekst jako string lematów
    lemma_text = " ".join(lemmas)
    
    # TF-IDF (single document, więc IDF nie ma sensu, ale TF tak)
    # Użyjemy prostszego podejścia - częstość słów
    vectorizer = TfidfVectorizer(
        max_features=n * 2,  # więcej na wszelki wypadek
        token_pattern=r"(?u)\b\w+\b"
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([lemma_text])
        feature_names = vectorizer.get_feature_names_out()
        
        # Pobierz scores
        scores = tfidf_matrix.toarray()[0]
        
        # Sortuj i weź top N
        word_scores = list(zip(feature_names, scores))
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        top_words = {word for word, score in word_scores[:n]}
        return top_words
        
    except ValueError:
        # Za mało słów
        return set(lemmas)


def calculate_keyword_overlap(keywords_a: set, keywords_b: set) -> float:
    """
    Oblicza overlap między dwoma zbiorami keywords.
    
    Args:
        keywords_a: Pierwszy zbiór keywords
        keywords_b: Drugi zbiór keywords
    
    Returns:
        Overlap jako procent (0-100)
    """
    if len(keywords_a) == 0 and len(keywords_b) == 0:
        return 100.0
    
    intersection = len(keywords_a & keywords_b)
    # Używamy średniej z dwóch zbiorów jako bazy
    avg_size = (len(keywords_a) + len(keywords_b)) / 2
    
    if avg_size == 0:
        return 0.0
    
    overlap = (intersection / avg_size) * 100
    return round(overlap, 2)


def process_single_article(article_name: str) -> dict:
    """Przetwarza pojedynczy artykuł i zwraca porównania."""
    # Pary do porównania
    version_pairs = list(combinations(VERSIONS, 2))
    
    # Wczytaj wszystkie wersje i wyodrębnij keywords
    version_keywords = {}
    
    for version in VERSIONS:
        try:
            data = load_article(article_name, version)
            content = data.get("content", "")
            keywords = get_top_keywords(content, TOP_N_KEYWORDS)
            version_keywords[version] = keywords
        except FileNotFoundError:
            pass  # Pominąć brakujące wersje
    
    # Oblicz overlap dla każdej pary
    comparisons = {}
    
    for v1, v2 in version_pairs:
        if v1 in version_keywords and v2 in version_keywords:
            overlap = calculate_keyword_overlap(
                version_keywords[v1], 
                version_keywords[v2]
            )
            key = f"{v1}__{v2}"
            comparisons[key] = overlap
    
    if comparisons:
        save_comparison_result(
            metric_name="tfidf_overlap",
            article_name=article_name,
            comparisons=comparisons,
            extra_data={"top_n_keywords": TOP_N_KEYWORDS}
        )
    
    return comparisons


def process_all_articles():
    """Przetwarza wszystkie artykuły i zapisuje wyniki."""
    aggregated = process_comparison_articles_parallel(
        metric_name="tfidf_overlap",
        process_article_func=process_single_article
    )
    
    # Zapisz agregowany JSON
    if aggregated:
        save_aggregated_comparison_metric("tfidf_overlap", aggregated)
    
    print("\nZakończono!")


if __name__ == "__main__":
    process_all_articles()

