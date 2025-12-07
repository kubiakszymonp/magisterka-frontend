"""
common.py - Wspólne narzędzia do analizy NLP artykułów

Ten moduł zawiera:
- Funkcje do wczytywania artykułów z data/articles/
- Funkcje do zapisywania wyników do output/
- Helpery do tokenizacji i przetwarzania tekstu polskiego
- Ładowanie modelu spaCy dla języka polskiego
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Generator

import spacy

# Ścieżki bazowe
BASE_DIR = Path(__file__).parent.parent
ARTICLES_DIR = BASE_DIR / "data" / "articles"
OUTPUT_DIR = Path(__file__).parent / "output"

# Wersje artykułów
VERSIONS = ["adult_full", "adult_short", "child_short"]

# Cache dla modelu spaCy
_nlp_model = None


def get_nlp():
    """
    Zwraca załadowany model spaCy dla języka polskiego.
    Model jest cache'owany dla wydajności.
    """
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("pl_core_news_sm")
        except OSError:
            print("Model pl_core_news_sm nie znaleziony, próbuję pl_core_news_lg...")
            try:
                _nlp_model = spacy.load("pl_core_news_lg")
            except OSError:
                raise RuntimeError(
                    "Brak modelu spaCy dla polskiego. Zainstaluj: "
                    "python -m spacy download pl_core_news_sm"
                )
    return _nlp_model


def list_articles() -> list[str]:
    """
    Zwraca listę nazw artykułów (nazwy folderów w data/articles/).
    """
    if not ARTICLES_DIR.exists():
        raise FileNotFoundError(f"Folder artykułów nie istnieje: {ARTICLES_DIR}")
    
    return [
        d.name for d in ARTICLES_DIR.iterdir() 
        if d.is_dir() and not d.name.startswith(".")
    ]


def load_article(article_name: str, version: str) -> dict:
    """
    Wczytuje pojedynczy artykuł.
    
    Args:
        article_name: Nazwa artykułu (folder)
        version: Wersja (adult_full, adult_short, child_short)
    
    Returns:
        Słownik z danymi artykułu (placeId, style, ageTarget, volume, title, content)
    """
    file_path = ARTICLES_DIR / article_name / f"{version}.json"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Artykuł nie istnieje: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_articles() -> Generator[tuple[str, str, dict], None, None]:
    """
    Generator zwracający wszystkie artykuły.
    
    Yields:
        Tuple (article_name, version, article_data)
    """
    for article_name in list_articles():
        for version in VERSIONS:
            try:
                data = load_article(article_name, version)
                yield article_name, version, data
            except FileNotFoundError:
                print(f"Pominięto brakujący plik: {article_name}/{version}.json")


def get_article_content(article_name: str, version: str) -> str:
    """
    Zwraca samą treść artykułu (pole content).
    """
    data = load_article(article_name, version)
    return data.get("content", "")


def save_metric_result(
    metric_name: str,
    article_name: str,
    version: str,
    value: Any,
    extra_data: dict | None = None
) -> Path:
    """
    Zapisuje wynik metryki do pliku JSON.
    
    Args:
        metric_name: Nazwa metryki (np. "word_count")
        article_name: Nazwa artykułu
        version: Wersja artykułu
        value: Wartość metryki
        extra_data: Dodatkowe dane do zapisania
    
    Returns:
        Ścieżka do zapisanego pliku
    """
    output_dir = OUTPUT_DIR / metric_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        "metric": metric_name,
        "article": article_name,
        "version": version,
        "value": value,
        "computed_at": datetime.now().isoformat()
    }
    
    if extra_data:
        result["extra"] = extra_data
    
    file_path = output_dir / f"{article_name}__{version}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return file_path


def save_comparison_result(
    metric_name: str,
    article_name: str,
    comparisons: dict[str, Any],
    extra_data: dict | None = None
) -> Path:
    """
    Zapisuje wynik porównania między wersjami do pliku JSON.
    
    Args:
        metric_name: Nazwa metryki (np. "jaccard_similarity")
        article_name: Nazwa artykułu
        comparisons: Słownik z porównaniami (np. {"adult_full__adult_short": 0.87})
        extra_data: Dodatkowe dane do zapisania
    
    Returns:
        Ścieżka do zapisanego pliku
    """
    output_dir = OUTPUT_DIR / metric_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        "metric": metric_name,
        "article": article_name,
        "comparisons": comparisons,
        "computed_at": datetime.now().isoformat()
    }
    
    if extra_data:
        result["extra"] = extra_data
    
    file_path = output_dir / f"{article_name}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return file_path


def save_aggregated_metric(
    metric_name: str,
    aggregated_data: dict[str, dict[str, Any]]
) -> Path:
    """
    Zapisuje agregowany JSON z wszystkimi wynikami metryki.
    
    Struktura:
    {
      "article_name": {
        "adult_full": value,
        "adult_short": value,
        "child_short": value
      },
      ...
    }
    
    Args:
        metric_name: Nazwa metryki
        aggregated_data: Słownik {article_name: {version: value}}
    
    Returns:
        Ścieżka do zapisanego pliku
    """
    output_dir = OUTPUT_DIR / metric_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        "metric": metric_name,
        "aggregated_at": datetime.now().isoformat(),
        "data": aggregated_data
    }
    
    file_path = output_dir / "aggregated.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return file_path


def save_aggregated_comparison_metric(
    metric_name: str,
    aggregated_data: dict[str, dict[str, Any]]
) -> Path:
    """
    Zapisuje agregowany JSON dla metryk porównawczych.
    
    Struktura:
    {
      "article_name": {
        "adult_full__adult_short": value,
        "adult_full__child_short": value,
        "adult_short__child_short": value
      },
      ...
    }
    
    Args:
        metric_name: Nazwa metryki
        aggregated_data: Słownik {article_name: {comparison_key: value}}
    
    Returns:
        Ścieżka do zapisanego pliku
    """
    output_dir = OUTPUT_DIR / metric_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        "metric": metric_name,
        "aggregated_at": datetime.now().isoformat(),
        "data": aggregated_data
    }
    
    file_path = output_dir / "aggregated.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return file_path


def get_tokens(text: str, lowercase: bool = True) -> list[str]:
    """
    Tokenizuje tekst używając spaCy.
    Zwraca tylko tokeny alfabetyczne (bez cyfr, interpunkcji).
    
    Args:
        text: Tekst do tokenizacji
        lowercase: Czy zamienić na małe litery
    
    Returns:
        Lista tokenów
    """
    nlp = get_nlp()
    doc = nlp(text)
    
    tokens = [
        token.text.lower() if lowercase else token.text
        for token in doc
        if token.is_alpha
    ]
    
    return tokens


def get_lemmas(text: str, lowercase: bool = True) -> list[str]:
    """
    Zwraca lematy (formy podstawowe) słów z tekstu.
    
    Args:
        text: Tekst do przetworzenia
        lowercase: Czy zamienić na małe litery
    
    Returns:
        Lista lematów
    """
    nlp = get_nlp()
    doc = nlp(text)
    
    lemmas = [
        token.lemma_.lower() if lowercase else token.lemma_
        for token in doc
        if token.is_alpha
    ]
    
    return lemmas


def get_sentences(text: str) -> list[str]:
    """
    Dzieli tekst na zdania używając spaCy.
    
    Args:
        text: Tekst do podziału
    
    Returns:
        Lista zdań
    """
    nlp = get_nlp()
    doc = nlp(text)
    
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def get_words_in_sentence(sentence: str) -> list[str]:
    """
    Zwraca słowa (tokeny alfabetyczne) z pojedynczego zdania.
    """
    nlp = get_nlp()
    doc = nlp(sentence)
    
    return [token.text for token in doc if token.is_alpha]


def count_syllables_polish(word: str) -> int:
    """
    Przybliżone liczenie sylab w słowie polskim.
    Bazuje na liczbie samogłosek (a, ą, e, ę, i, o, ó, u, y).
    
    Args:
        word: Słowo do analizy
    
    Returns:
        Przybliżona liczba sylab
    """
    vowels = set("aąeęioóuy")
    word_lower = word.lower()
    
    count = sum(1 for char in word_lower if char in vowels)
    
    # Minimum 1 sylaba dla każdego słowa
    return max(1, count)


def get_content_words(text: str) -> list[str]:
    """
    Zwraca słowa treściowe (rzeczowniki, czasowniki, przymiotniki, przysłówki).
    Używane do obliczania lexical density.
    
    Args:
        text: Tekst do analizy
    
    Returns:
        Lista słów treściowych
    """
    nlp = get_nlp()
    doc = nlp(text)
    
    # POS tags dla słów treściowych
    content_pos = {"NOUN", "VERB", "ADJ", "ADV"}
    
    return [
        token.text.lower()
        for token in doc
        if token.is_alpha and token.pos_ in content_pos
    ]


if __name__ == "__main__":
    # Test - wyświetl listę artykułów
    print("Dostępne artykuły:")
    for article in list_articles():
        print(f"  - {article}")
    
    print(f"\nŚcieżka output: {OUTPUT_DIR}")

