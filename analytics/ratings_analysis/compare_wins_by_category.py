"""
Wykres #7: Ranking zwycięstw według kategorii

OPIS WYKRESU:
Grouped bar chart pokazujący ile razy każdy typ artykułu został wybrany
jako najlepszy w każdej kategorii porównania.

CO PORÓWNUJE:
- Który styl wygrywa w której kategorii
- bestOverall, easiestToUnderstand, bestForChildren, bestForQuickLook, bestForPlanning

INTERPRETACJA:
- Wyższe słupki = więcej zwycięstw
- Pozwala zobaczyć mocne strony każdego typu artykułu
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_compare_ratings, count_compare_wins, setup_polish_matplotlib, save_chart,
    get_ordered_versions, VERSION_LABELS, VERSION_COLORS,
    COMPARE_CATEGORIES, COMPARE_CATEGORY_LABELS
)
import numpy as np


def create_wins_by_category_chart():
    plt = setup_polish_matplotlib()
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_compare_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} porównań z ankiety compare")
    
    # Zlicz zwycięstwa dla każdej kategorii
    wins_by_category = {}
    for category in COMPARE_CATEGORIES:
        wins_by_category[category] = count_compare_wins(data, category)
    
    # ===== WYKRES 1: Grouped bar chart - wszystkie kategorie =====
    fig, ax = plt.subplots(figsize=(16, 8))
    
    x = np.arange(len(COMPARE_CATEGORIES))
    width = 0.25
    offsets = [-width, 0, width]
    
    for i, version in enumerate(versions):
        values = [wins_by_category[cat][version] for cat in COMPARE_CATEGORIES]
        bars = ax.bar(x + offsets[i], values, width,
                     label=VERSION_LABELS[version],
                     color=VERSION_COLORS[version],
                     edgecolor='black', linewidth=1)
        
        # Dodaj wartości na słupkach
        for bar, val in zip(bars, values):
            if val > 0:
                ax.annotate(f'{val}',
                           xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                           xytext=(0, 3), textcoords='offset points',
                           ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Kategoria porównania', fontsize=12, fontweight='bold')
    ax.set_ylabel('Liczba zwycięstw', fontsize=12, fontweight='bold')
    ax.set_title(f'Liczba zwycięstw według kategorii porównania\n(n={len(data)} porównań)', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([COMPARE_CATEGORY_LABELS[c] for c in COMPARE_CATEGORIES], 
                       rotation=20, ha='right')
    
    # Legenda po prawej stronie
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', 
                            label=VERSION_LABELS[v]) for v in versions]
    ax.legend(handles=legend_elements, title='Typ artykułu', 
              loc='upper right', bbox_to_anchor=(1.2, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "compare_wins_by_category")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - ZWYCIĘSTWA WG KATEGORII")
    print("="*60)
    
    for category in COMPARE_CATEGORIES:
        print(f"\n{COMPARE_CATEGORY_LABELS[category]}:")
        total = sum(wins_by_category[category][v] for v in versions)
        for version in versions:
            count = wins_by_category[category][version]
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {VERSION_LABELS[version]}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    create_wins_by_category_chart()

