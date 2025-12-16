"""
Wykres S-D: Ocena długości według typu artykułu

OPIS WYKRESU:
Stacked bar chart pokazujący rozkład procentowy ocen długości
(za krótki / w sam raz / za długi) dla każdego typu artykułu.

CO PORÓWNUJE:
- Jak użytkownicy postrzegają długość każdego typu artykułu
- Czy adult_full jest faktycznie za długi dla czytelników

INTERPRETACJA:
- Więcej zielonego (w sam raz) = optymalna długość
- Dużo czerwonego (za długi) = artykuł należy skrócić
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_single_ratings, setup_polish_matplotlib, save_chart, 
    get_ordered_versions, VERSION_LABELS, VERSION_COLORS,
    LENGTH_VALUES, LENGTH_LABELS, LENGTH_COLORS
)
import numpy as np


def create_length_perception_chart():
    plt = setup_polish_matplotlib()
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_single_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} ocen z ankiety single")
    
    # Zlicz oceny długości dla każdego stylu
    length_counts = {v: {l: 0 for l in LENGTH_VALUES} for v in versions}
    totals = {v: 0 for v in versions}
    
    for entry in data:
        style = entry.get("articleStyle")
        length = entry.get("length")
        if style in versions and length in LENGTH_VALUES:
            length_counts[style][length] += 1
            totals[style] += 1
    
    # Przelicz na procenty
    length_percentages = {v: {} for v in versions}
    for v in versions:
        for l in LENGTH_VALUES:
            if totals[v] > 0:
                length_percentages[v][l] = (length_counts[v][l] / totals[v]) * 100
            else:
                length_percentages[v][l] = 0
    
    # ===== WYKRES 1: Stacked bar chart (100%) =====
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(versions))
    width = 0.6
    
    bottoms = np.zeros(len(versions))
    
    for length_val in LENGTH_VALUES:
        values = [length_percentages[v][length_val] for v in versions]
        bars = ax.bar(x, values, width, bottom=bottoms, 
                     label=LENGTH_LABELS[length_val],
                     color=LENGTH_COLORS[length_val],
                     edgecolor='black', linewidth=1)
        
        # Dodaj etykiety procentowe
        for i, (bar, val) in enumerate(zip(bars, values)):
            if val > 5:  # Pokaż tylko jeśli > 5%
                ax.text(bar.get_x() + bar.get_width()/2, 
                       bottoms[i] + val/2,
                       f'{val:.1f}%', ha='center', va='center', 
                       fontsize=10, fontweight='bold',
                       color='white' if length_val != 'just_right' else 'black')
        
        bottoms += values
    
    ax.set_xlabel('Typ artykułu', fontsize=12, fontweight='bold')
    ax.set_ylabel('Procent odpowiedzi', fontsize=12, fontweight='bold')
    ax.set_title(f'Postrzeganie długości artykułów\n(n={len(data)} ocen)', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([VERSION_LABELS[v] for v in versions])
    ax.set_ylim(0, 105)
    
    # Legenda po prawej stronie
    legend_elements = [Patch(facecolor=LENGTH_COLORS[l], edgecolor='black', 
                            label=LENGTH_LABELS[l]) for l in LENGTH_VALUES]
    ax.legend(handles=legend_elements, title='Ocena długości', 
              loc='upper right', bbox_to_anchor=(1.22, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "single_length_perception_stacked")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - POSTRZEGANIE DŁUGOŚCI")
    print("="*60)
    
    for version in versions:
        print(f"\n{VERSION_LABELS[version]} (n={totals[version]}):")
        for length_val in LENGTH_VALUES:
            count = length_counts[version][length_val]
            pct = length_percentages[version][length_val]
            print(f"  {LENGTH_LABELS[length_val]}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    create_length_perception_chart()

