"""
Wspólne funkcje dla wszystkich skryptów wykresów.
Używane do wczytywania danych i tworzenia spójnych wizualizacji.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np

# Konfiguracja ścieżek
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_OUTPUT_DIR = Path(__file__).parent / "output"

# Nazwy wersji tekstów (do wyświetlania)
VERSION_LABELS = {
    "child_short": "Dziecięca (krótka)",
    "adult_short": "Dorosła (krótka)", 
    "adult_full": "Dorosła (pełna)"
}

# Kolory dla wersji - spójna paleta
VERSION_COLORS = {
    "child_short": "#4CAF50",    # Zielony - przyjazny dla dzieci
    "adult_short": "#2196F3",    # Niebieski - dorosły, krótki
    "adult_full": "#9C27B0"      # Fioletowy - dorosły, pełny
}

# Kolory dla porównań par
PAIR_COLORS = {
    "adult_full__adult_short": "#E91E63",   # Różowy
    "adult_full__child_short": "#FF9800",   # Pomarańczowy
    "adult_short__child_short": "#00BCD4"   # Turkusowy
}

PAIR_LABELS = {
    "adult_full__adult_short": "Pełna ↔ Krótka (dorosła)",
    "adult_full__child_short": "Pełna ↔ Dziecięca",
    "adult_short__child_short": "Krótka (dorosła) ↔ Dziecięca"
}


def load_aggregated_data(metric_name: str) -> Dict[str, Any]:
    """Wczytuje zagregowane dane dla danej metryki."""
    filepath = OUTPUT_DIR / metric_name / "aggregated.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def aggregate_by_version(data: Dict[str, Any], value_key: str = None) -> Dict[str, List[float]]:
    """
    Agreguje wartości według wersji tekstu.
    
    Args:
        data: Słownik z danymi (artykuł -> wersja -> wartość)
        value_key: Klucz wartości jeśli wartość jest słownikiem (np. dla TTR)
    
    Returns:
        Słownik {wersja: [lista wartości ze wszystkich artykułów]}
    """
    versions = {}
    
    for article, article_data in data.items():
        for version, value in article_data.items():
            if version not in versions:
                versions[version] = []
            
            if value_key and isinstance(value, dict):
                versions[version].append(value[value_key])
            else:
                versions[version].append(value)
    
    return versions


def aggregate_pairs(data: Dict[str, Any]) -> Dict[str, List[float]]:
    """
    Agreguje wartości dla metryk porównawczych (pary wersji).
    
    Returns:
        Słownik {para: [lista wartości]}
    """
    pairs = {}
    
    for article, article_data in data.items():
        for pair, value in article_data.items():
            if pair not in pairs:
                pairs[pair] = []
            pairs[pair].append(value)
    
    return pairs


def calculate_stats(values: List[float]) -> Dict[str, float]:
    """Oblicza statystyki opisowe dla listy wartości."""
    arr = np.array(values)
    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "median": float(np.median(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "q25": float(np.percentile(arr, 25)),
        "q75": float(np.percentile(arr, 75))
    }


def setup_polish_matplotlib():
    """Konfiguruje matplotlib dla polskiego tekstu."""
    import matplotlib.pyplot as plt
    import matplotlib
    
    # Użyj fontów obsługujących polskie znaki
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
    
    # Styl naukowy
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'
    
    # Czcionki
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    
    # Grid
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    
    return plt


def save_chart(fig, filename: str, formats: List[str] = ['png', 'pdf']):
    """Zapisuje wykres w wielu formatach."""
    CHARTS_OUTPUT_DIR.mkdir(exist_ok=True)
    
    for fmt in formats:
        filepath = CHARTS_OUTPUT_DIR / f"{filename}.{fmt}"
        fig.savefig(filepath, format=fmt, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', dpi=300)
    
    print(f"  ✓ Zapisano: {filename}.{{{', '.join(formats)}}}")


def get_ordered_versions() -> List[str]:
    """Zwraca wersje w logicznej kolejności."""
    return ["child_short", "adult_short", "adult_full"]


def get_ordered_pairs() -> List[str]:
    """Zwraca pary w logicznej kolejności."""
    return ["adult_full__adult_short", "adult_full__child_short", "adult_short__child_short"]


def format_article_name(name: str) -> str:
    """Formatuje nazwę artykułu do wyświetlenia."""
    return name.replace("_", " ").title()[:30]


if __name__ == "__main__":
    # Test - sprawdź czy dane się wczytują
    for metric in ["word_count", "ttr", "readability", "jaccard_similarity"]:
        try:
            data = load_aggregated_data(metric)
            print(f"✓ {metric}: {len(data['data'])} artykułów")
        except Exception as e:
            print(f"✗ {metric}: {e}")

