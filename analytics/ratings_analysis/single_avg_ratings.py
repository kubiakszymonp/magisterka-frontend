"""
Wykres #1: Średnie ocen według typu generacji (articleStyle)

OPIS WYKRESU:
Grouped bar chart pokazujący średnie wartości każdej oceny (clarity, styleMatch,
structure, usefulness, enjoyment) dla każdego typu artykułu.

CO PORÓWNUJE:
- Jak różne style artykułów są oceniane w każdym wymiarze jakości
- Średnie ± odchylenie standardowe

INTERPRETACJA:
- Wyższe słupki = lepsze oceny
- Porównanie pozwala zobaczyć mocne/słabe strony każdego stylu
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_single_ratings, aggregate_single_by_style, calculate_stats,
    setup_polish_matplotlib, save_chart, get_ordered_versions,
    VERSION_LABELS, VERSION_COLORS, RATING_FIELDS, RATING_LABELS
)
import numpy as np


def create_avg_ratings_chart():
    plt = setup_polish_matplotlib()
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_single_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} ocen z ankiety single")
    
    # ===== WYKRES 1: Grouped bar chart - wszystkie oceny =====
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(RATING_FIELDS))
    width = 0.25
    offsets = [-width, 0, width]
    
    for i, version in enumerate(versions):
        by_style = aggregate_single_by_style(data, RATING_FIELDS[0])
        
        means = []
        stds = []
        
        for field in RATING_FIELDS:
            by_style = aggregate_single_by_style(data, field)
            values = by_style[version]
            if values:
                means.append(np.mean(values))
                stds.append(np.std(values))
            else:
                means.append(0)
                stds.append(0)
        
        bars = ax.bar(x + offsets[i], means, width, 
                     yerr=stds, capsize=3,
                     label=VERSION_LABELS[version],
                     color=VERSION_COLORS[version],
                     edgecolor='black', linewidth=1,
                     error_kw={'linewidth': 1.5, 'capthick': 1.5})
        
        # Dodaj wartości na słupkach
        for bar, mean in zip(bars, means):
            ax.annotate(f'{mean:.2f}',
                       xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 3), textcoords='offset points',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Kategoria oceny', fontsize=12, fontweight='bold')
    ax.set_ylabel('Średnia ocena (1-5)', fontsize=12, fontweight='bold')
    ax.set_title(f'Średnie oceny według typu artykułu\n(n={len(data)} ocen, skala 1-5)', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([RATING_LABELS[f] for f in RATING_FIELDS], rotation=15, ha='right')
    ax.set_ylim(0, 5.8)
    ax.axhline(y=3, color='gray', linestyle='--', alpha=0.5, label='Średnia neutralna')
    
    # Legenda po prawej stronie
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax.legend(handles=legend_elements, title='Typ artykułu', 
              loc='upper right', bbox_to_anchor=(1.22, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "single_avg_ratings_by_style")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - ŚREDNIE OCEN WG TYPU ARTYKUŁU")
    print("="*60)
    
    for version in versions:
        print(f"\n{VERSION_LABELS[version]}:")
        for field in RATING_FIELDS:
            by_style = aggregate_single_by_style(data, field)
            if by_style[version]:
                stats = calculate_stats(by_style[version])
                print(f"  {RATING_LABELS[field]}: {stats['mean']:.2f} ± {stats['std']:.2f} (n={stats['count']})")


if __name__ == "__main__":
    create_avg_ratings_chart()

