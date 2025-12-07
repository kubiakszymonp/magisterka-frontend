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
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Callable, Generator

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


def _process_single_article(
    article_name: str,
    version: str,
    metric_name: str,
    calculate_func: Callable[[str], Any],
    extra_data_func: Callable[[str], dict] | None = None
) -> tuple[str, str, Any, dict | None]:
    """
    Funkcja pomocnicza do przetwarzania pojedynczego artykułu.
    Używana w równoległym przetwarzaniu - musi być na poziomie modułu.
    
    Args:
        article_name: Nazwa artykułu
        version: Wersja artykułu
        metric_name: Nazwa metryki
        calculate_func: Funkcja obliczająca metrykę (tekst -> wartość)
        extra_data_func: Opcjonalna funkcja zwracająca dodatkowe dane
    
    Returns:
        Tuple (article_name, version, value, extra_data)
    """
    try:
        data = load_article(article_name, version)
        content = data.get("content", "")
        
        value = calculate_func(content)
        
        extra_data = None
        if extra_data_func:
            extra_data = extra_data_func(content)
        
        save_metric_result(
            metric_name=metric_name,
            article_name=article_name,
            version=version,
            value=value,
            extra_data=extra_data
        )
        
        return (article_name, version, value, extra_data)
    except FileNotFoundError:
        return (article_name, version, None, None)


def process_articles_parallel(
    metric_name: str,
    calculate_func: Callable[[str], Any],
    extra_data_func: Callable[[str], dict] | None = None,
    max_workers: int | None = None
) -> dict[str, dict[str, Any]]:
    """
    Przetwarza wszystkie artykuły równolegle używając wielu procesów.
    
    Args:
        metric_name: Nazwa metryki (np. "word_count")
        calculate_func: Funkcja obliczająca metrykę dla tekstu (tekst -> wartość)
        extra_data_func: Opcjonalna funkcja zwracająca dodatkowe dane dla każdego artykułu
        max_workers: Liczba procesów (None = liczba CPU)
    
    Returns:
        Słownik {article_name: {version: value}} z wynikami
    """
    articles = list_articles()
    
    print(f"Przetwarzanie {len(articles)} artykułów (równolegle, {max_workers or 'auto'} procesów)...")
    
    # Przygotuj listę zadań
    tasks = []
    for article_name in articles:
        for version in VERSIONS:
            tasks.append((article_name, version))
    
    aggregated = {article_name: {} for article_name in articles}
    
    # Przetwarzaj równolegle
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Utwórz funkcję częściową z parametrami
        process_func = partial(
            _process_single_article,
            metric_name=metric_name,
            calculate_func=calculate_func,
            extra_data_func=extra_data_func
        )
        
        # Wyślij wszystkie zadania
        future_to_task = {
            executor.submit(process_func, article_name, version): (article_name, version)
            for article_name, version in tasks
        }
        
        # Zbierz wyniki
        completed = 0
        for future in as_completed(future_to_task):
            article_name, version = future_to_task[future]
            try:
                result_article, result_version, value, extra_data = future.result()
                
                if value is not None:
                    aggregated[result_article][result_version] = value
                    # Formatuj wartość dla wyświetlenia
                    if isinstance(value, dict):
                        value_str = ", ".join(f"{k}={v}" for k, v in value.items())
                        print(f"  {result_article}/{result_version}: {value_str}")
                    else:
                        print(f"  {result_article}/{result_version}: {value}")
                else:
                    print(f"  POMINIĘTO: {article_name}/{version} (brak pliku)")
                
                completed += 1
            except Exception as e:
                print(f"  BŁĄD: {article_name}/{version}: {e}")
                completed += 1
    
    return aggregated


def _process_comparison_article(
    article_name: str,
    metric_name: str,
    process_func: Callable[[str], dict]
) -> tuple[str, dict | None]:
    """
    Funkcja pomocnicza do przetwarzania pojedynczego artykułu dla metryk porównawczych.
    Używana w równoległym przetwarzaniu - musi być na poziomie modułu.
    
    Args:
        article_name: Nazwa artykułu
        metric_name: Nazwa metryki
        process_func: Funkcja przetwarzająca artykuł (article_name -> comparisons dict)
    
    Returns:
        Tuple (article_name, comparisons dict lub None)
    """
    try:
        comparisons = process_func(article_name)
        if comparisons:
            # Funkcja process_func powinna sama zapisać wyniki
            return (article_name, comparisons)
        return (article_name, None)
    except Exception as e:
        print(f"  BŁĄD w {article_name}: {e}")
        return (article_name, None)


def process_comparison_articles_parallel(
    metric_name: str,
    process_article_func: Callable[[str], dict],
    max_workers: int | None = None
) -> dict[str, dict[str, Any]]:
    """
    Przetwarza wszystkie artykuły równolegle dla metryk porównawczych.
    
    Args:
        metric_name: Nazwa metryki (np. "jaccard_similarity")
        process_article_func: Funkcja przetwarzająca pojedynczy artykuł
            (article_name -> comparisons dict)
        max_workers: Liczba procesów (None = liczba CPU)
    
    Returns:
        Słownik {article_name: comparisons} z wynikami
    """
    articles = list_articles()
    
    print(f"Przetwarzanie {len(articles)} artykułów (równolegle, {max_workers or 'auto'} procesów)...")
    
    aggregated = {}
    
    # Przetwarzaj równolegle
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Utwórz funkcję częściową z parametrami
        process_func = partial(
            _process_comparison_article,
            metric_name=metric_name,
            process_func=process_article_func
        )
        
        # Wyślij wszystkie zadania
        future_to_article = {
            executor.submit(process_func, article_name): article_name
            for article_name in articles
        }
        
        # Zbierz wyniki
        for future in as_completed(future_to_article):
            article_name = future_to_article[future]
            try:
                result_article, comparisons = future.result()
                
                if comparisons is not None:
                    aggregated[result_article] = comparisons
                    print(f"  {result_article}:")
                    for key, val in comparisons.items():
                        if isinstance(val, float):
                            print(f"    {key}: {val}")
                        else:
                            print(f"    {key}: {val}")
                else:
                    print(f"  POMINIĘTO: {article_name}")
                    
            except Exception as e:
                print(f"  BŁĄD: {article_name}: {e}")
    
    return aggregated


if __name__ == "__main__":
    # Test - wyświetl listę artykułów
    print("Dostępne artykuły:")
    for article in list_articles():
        print(f"  - {article}")
    
    print(f"\nŚcieżka output: {OUTPUT_DIR}")

