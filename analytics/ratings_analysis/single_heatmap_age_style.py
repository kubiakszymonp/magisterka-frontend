"""
Wykres #4: Heatmapa ageGroup × articleStyle

OPIS WYKRESU:
Heatmapa pokazująca średnią ocenę (ze wszystkich kategorii) dla każdej 
kombinacji grupy wiekowej i typu artykułu.

CO PORÓWNUJE:
- Jak różne grupy wiekowe oceniają różne style artykułów
- Interakcję między wiekiem czytelnika a typem treści

INTERPRETACJA:
- Ciemniejsze kolory = wyższe oceny
- Pozwala zobaczyć czy młodsi wolą child_short, a starsi adult_full
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_single_ratings, setup_polish_matplotlib, save_chart, 
    get_ordered_versions, VERSION_LABELS, VERSION_COLORS,
    AGE_GROUPS, AGE_GROUP_LABELS, RATING_FIELDS, RATING_LABELS
)
import numpy as np


def create_heatmap_age_style():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    data = load_single_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} ocen z ankiety single")
    
    # ===== WYKRES 1: Heatmapa średniej wszystkich ocen =====
    # Przygotuj macierz danych
    matrix = np.zeros((len(AGE_GROUPS), len(versions)))
    counts = np.zeros((len(AGE_GROUPS), len(versions)))
    
    for entry in data:
        age_idx = AGE_GROUPS.index(entry["ageGroup"]) if entry["ageGroup"] in AGE_GROUPS else -1
        style_idx = versions.index(entry["articleStyle"]) if entry["articleStyle"] in versions else -1
        
        if age_idx >= 0 and style_idx >= 0:
            # Średnia z wszystkich ocen dla tego wpisu
            ratings = [entry.get(f, 0) for f in RATING_FIELDS if entry.get(f) is not None]
            if ratings:
                matrix[age_idx, style_idx] += np.mean(ratings)
                counts[age_idx, style_idx] += 1
    
    # Oblicz średnie (unikaj dzielenia przez zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_matrix = np.divide(matrix, counts)
        avg_matrix = np.nan_to_num(avg_matrix, nan=0)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Heatmapa
    im = ax.imshow(avg_matrix, cmap='RdYlGn', aspect='auto', vmin=1, vmax=5)
    
    # Etykiety
    ax.set_xticks(np.arange(len(versions)))
    ax.set_yticks(np.arange(len(AGE_GROUPS)))
    ax.set_xticklabels([VERSION_LABELS[v] for v in versions], fontsize=11)
    ax.set_yticklabels([AGE_GROUP_LABELS[ag] for ag in AGE_GROUPS], fontsize=11)
    
    ax.set_xlabel('Typ artykułu', fontsize=12, fontweight='bold')
    ax.set_ylabel('Grupa wiekowa', fontsize=12, fontweight='bold')
    ax.set_title(f'Średnia ocena wg grupy wiekowej i typu artykułu\n(n={len(data)} ocen, skala 1-5)', 
                fontsize=14, fontweight='bold', pad=15)
    
    # Dodaj wartości w komórkach
    for i in range(len(AGE_GROUPS)):
        for j in range(len(versions)):
            val = avg_matrix[i, j]
            count = int(counts[i, j])
            if count > 0:
                text_color = 'white' if val < 2.5 or val > 4 else 'black'
                ax.text(j, i, f'{val:.2f}\n(n={count})', 
                       ha='center', va='center', fontsize=10, color=text_color, fontweight='bold')
    
    # Colorbar po prawej stronie
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Średnia ocena (1-5)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig, "single_heatmap_age_style")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - HEATMAPA WIEK × STYL")
    print("="*60)
    print("\nŚrednia ocen (wszystkie kategorie):")
    print(f"{'Wiek':<15}", end="")
    for v in versions:
        print(f"{VERSION_LABELS[v]:<20}", end="")
    print()
    
    for i, ag in enumerate(AGE_GROUPS):
        print(f"{AGE_GROUP_LABELS[ag]:<15}", end="")
        for j in range(len(versions)):
            if counts[i, j] > 0:
                print(f"{avg_matrix[i, j]:.2f} (n={int(counts[i, j]):<3})", end="   ")
            else:
                print(f"{'brak danych':<17}", end="   ")
        print()


if __name__ == "__main__":
    create_heatmap_age_style()

