"""
Wykres #9: Preferencje według grupy wiekowej

OPIS WYKRESU:
Stacked bar chart pokazujący jakie typy artykułów preferują różne 
grupy wiekowe (na podstawie wyboru bestOverall).

CO PORÓWNUJE:
- Czy młodsi wybierają child_short
- Czy starsi preferują adult_full
- Wzorce preferencji w różnych grupach wiekowych

INTERPRETACJA:
- Pozwala zobaczyć czy artykuły trafiają do właściwej grupy docelowej
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_compare_ratings, setup_polish_matplotlib, save_chart,
    get_ordered_versions, VERSION_LABELS, VERSION_COLORS,
    AGE_GROUPS, AGE_GROUP_LABELS, COMPARE_CATEGORIES, COMPARE_CATEGORY_LABELS
)
import numpy as np


def create_preferences_by_age_chart():
    plt = setup_polish_matplotlib()
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_compare_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} porównań z ankiety compare")
    
    # Zlicz preferencje (bestOverall) według grupy wiekowej
    prefs_by_age = {ag: {v: 0 for v in versions} for ag in AGE_GROUPS}
    totals_by_age = {ag: 0 for ag in AGE_GROUPS}
    
    for entry in data:
        age = entry.get("ageGroup")
        choice = entry.get("bestOverall")
        if age in AGE_GROUPS and choice in versions:
            prefs_by_age[age][choice] += 1
            totals_by_age[age] += 1
    
    # Filtruj grupy wiekowe z danymi
    active_age_groups = [ag for ag in AGE_GROUPS if totals_by_age[ag] > 0]
    
    # ===== WYKRES 1: Stacked bar chart (100%) =====
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(active_age_groups))
    width = 0.7
    
    bottoms = np.zeros(len(active_age_groups))
    
    for version in versions:
        values = []
        for ag in active_age_groups:
            if totals_by_age[ag] > 0:
                values.append((prefs_by_age[ag][version] / totals_by_age[ag]) * 100)
            else:
                values.append(0)
        
        bars = ax.bar(x, values, width, bottom=bottoms,
                     label=VERSION_LABELS[version],
                     color=VERSION_COLORS[version],
                     edgecolor='black', linewidth=1)
        
        # Etykiety procentowe
        for i, (bar, val) in enumerate(zip(bars, values)):
            if val > 8:
                ax.text(bar.get_x() + bar.get_width()/2,
                       bottoms[i] + val/2,
                       f'{val:.0f}%', ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white')
        
        bottoms += values
    
    ax.set_xlabel('Grupa wiekowa', fontsize=12, fontweight='bold')
    ax.set_ylabel('Procent wyborów', fontsize=12, fontweight='bold')
    ax.set_title(f'Preferencje "najlepsza wersja ogólnie" według grupy wiekowej\n(n={len(data)} porównań)', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{AGE_GROUP_LABELS[ag]}\n(n={totals_by_age[ag]})" for ag in active_age_groups])
    ax.set_ylim(0, 105)
    
    # Legenda po prawej stronie
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', 
                            label=VERSION_LABELS[v]) for v in versions]
    ax.legend(handles=legend_elements, title='Typ artykułu', 
              loc='upper left', bbox_to_anchor=(1.02, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "compare_preferences_by_age_stacked")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - PREFERENCJE WG GRUPY WIEKOWEJ")
    print("="*60)
    
    for ag in active_age_groups:
        print(f"\n{AGE_GROUP_LABELS[ag]} (n={totals_by_age[ag]}):")
        for version in versions:
            count = prefs_by_age[ag][version]
            pct = (count / totals_by_age[ag] * 100) if totals_by_age[ag] > 0 else 0
            bar = "█" * int(pct / 5)
            print(f"  {VERSION_LABELS[version]}: {count:2d} ({pct:5.1f}%) {bar}")


if __name__ == "__main__":
    create_preferences_by_age_chart()

