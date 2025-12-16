"""
Wspólne funkcje dla analizy ratingów z ankiet.
Wczytuje dane z data/ratings/single.json i data/ratings/compare.json.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import numpy as np

# Konfiguracja ścieżek
BASE_DIR = Path(__file__).parent.parent.parent
RATINGS_DIR = BASE_DIR / "data" / "ratings"
CHARTS_OUTPUT_DIR = Path(__file__).parent / "output"

# Pliki z danymi
SINGLE_RATINGS_FILE = RATINGS_DIR / "single.json"
COMPARE_RATINGS_FILE = RATINGS_DIR / "compare.json"

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

# Grupy wiekowe
AGE_GROUPS = ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "60+"]
AGE_GROUP_LABELS = {
    "1-10": "1-10 lat",
    "11-20": "11-20 lat",
    "21-30": "21-30 lat",
    "31-40": "31-40 lat",
    "41-50": "41-50 lat",
    "51-60": "51-60 lat",
    "60+": "60+ lat"
}

AGE_GROUP_COLORS = {
    "1-10": "#FF6B6B",
    "11-20": "#4ECDC4",
    "21-30": "#45B7D1",
    "31-40": "#96CEB4",
    "41-50": "#FFEAA7",
    "51-60": "#DDA0DD",
    "60+": "#98D8C8"
}

# Nazwy ocen w ankiecie single
RATING_FIELDS = ["clarity", "styleMatch", "structure", "usefulness", "enjoyment"]
RATING_LABELS = {
    "clarity": "Przejrzystość",
    "styleMatch": "Dopasowanie stylu",
    "structure": "Struktura",
    "usefulness": "Użyteczność",
    "enjoyment": "Przyjemność czytania"
}

# Nazwy kategorii w ankiecie compare
COMPARE_CATEGORIES = ["bestOverall", "easiestToUnderstand", "bestForChildren", "bestForQuickLook", "bestForPlanning"]
COMPARE_CATEGORY_LABELS = {
    "bestOverall": "Najlepsza ogólnie",
    "easiestToUnderstand": "Najłatwiejsza do zrozumienia",
    "bestForChildren": "Najlepsza dla dzieci",
    "bestForQuickLook": "Najlepsza na szybki przegląd",
    "bestForPlanning": "Najlepsza do planowania"
}

# Ocena długości
LENGTH_VALUES = ["too_short", "just_right", "too_long"]
LENGTH_LABELS = {
    "too_short": "Za krótki",
    "just_right": "W sam raz",
    "too_long": "Za długi"
}
LENGTH_COLORS = {
    "too_short": "#FFA726",  # Pomarańczowy
    "just_right": "#66BB6A",  # Zielony
    "too_long": "#EF5350"    # Czerwony
}


def load_single_ratings() -> List[Dict[str, Any]]:
    """Wczytuje dane z ankiety single (oceny pojedynczych artykułów)."""
    with open(SINGLE_RATINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_compare_ratings() -> List[Dict[str, Any]]:
    """Wczytuje dane z ankiety compare (porównania między wersjami)."""
    with open(COMPARE_RATINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_ordered_versions() -> List[str]:
    """Zwraca wersje w logicznej kolejności."""
    return ["child_short", "adult_short", "adult_full"]


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
        "q75": float(np.percentile(arr, 75)),
        "count": len(values)
    }


def setup_polish_matplotlib():
    """Konfiguruje matplotlib dla polskiego tekstu."""
    import matplotlib.pyplot as plt
    
    # Użyj fontów obsługujących polskie znaki
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
    
    # Styl naukowy
    plt.rcParams['figure.figsize'] = (12, 7)
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


def save_chart(fig, filename: str, formats: List[str] = ['png']):
    """Zapisuje wykres w wielu formatach."""
    CHARTS_OUTPUT_DIR.mkdir(exist_ok=True)
    
    for fmt in formats:
        filepath = CHARTS_OUTPUT_DIR / f"{filename}.{fmt}"
        fig.savefig(filepath, format=fmt, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', dpi=300)
    
    print(f"  ✓ Zapisano: {filename}.{{{', '.join(formats)}}}")


def aggregate_single_by_style(data: List[Dict], field: str) -> Dict[str, List[float]]:
    """
    Agreguje wartości z ankiety single według stylu artykułu.
    
    Args:
        data: Lista ocen z ankiety single
        field: Nazwa pola do agregacji (np. 'clarity', 'enjoyment')
    
    Returns:
        Słownik {articleStyle: [lista wartości]}
    """
    result = {v: [] for v in get_ordered_versions()}
    
    for entry in data:
        style = entry.get("articleStyle")
        value = entry.get(field)
        if style in result and value is not None:
            result[style].append(value)
    
    return result


def aggregate_single_by_age(data: List[Dict], field: str) -> Dict[str, List[float]]:
    """
    Agreguje wartości z ankiety single według grupy wiekowej.
    
    Args:
        data: Lista ocen z ankiety single
        field: Nazwa pola do agregacji
    
    Returns:
        Słownik {ageGroup: [lista wartości]}
    """
    result = {ag: [] for ag in AGE_GROUPS}
    
    for entry in data:
        age = entry.get("ageGroup")
        value = entry.get(field)
        if age in result and value is not None:
            result[age].append(value)
    
    return result


def count_compare_wins(data: List[Dict], category: str) -> Dict[str, int]:
    """
    Liczy zwycięstwa każdego stylu w danej kategorii porównania.
    
    Args:
        data: Lista ocen z ankiety compare
        category: Kategoria (np. 'bestOverall')
    
    Returns:
        Słownik {articleStyle: liczba_zwycięstw}
    """
    result = {v: 0 for v in get_ordered_versions()}
    
    for entry in data:
        winner = entry.get(category)
        if winner in result:
            result[winner] += 1
    
    return result


if __name__ == "__main__":
    # Test - sprawdź czy dane się wczytują
    single = load_single_ratings()
    compare = load_compare_ratings()
    
    print(f"✓ Single ratings: {len(single)} wpisów")
    print(f"✓ Compare ratings: {len(compare)} wpisów")
    
    # Pokaż strukturę
    if single:
        print(f"\nPrzykładowy wpis single:")
        for key in single[0]:
            print(f"  - {key}: {single[0][key]}")
    
    if compare:
        print(f"\nPrzykładowy wpis compare:")
        for key in compare[0]:
            print(f"  - {key}: {compare[0][key]}")

