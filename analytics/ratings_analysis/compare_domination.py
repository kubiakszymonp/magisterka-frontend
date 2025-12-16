"""
Wykres C-B: Analiza dominacji

OPIS WYKRESU:
Pie chart pokazujący ile procent respondentów wybrało TEN SAM typ artykułu
we wszystkich 5 kategoriach porównania (pełna dominacja jednego stylu).

CO PORÓWNUJE:
- Czy ludzie mają jednego faworyta we wszystkich kategoriach
- Spójność preferencji

INTERPRETACJA:
- Wysoki % dominacji = silne preferencje dla jednego stylu
- Niski % = różne style są lepsze w różnych kontekstach
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_compare_ratings, setup_polish_matplotlib, save_chart,
    get_ordered_versions, VERSION_LABELS, VERSION_COLORS,
    COMPARE_CATEGORIES
)
import numpy as np


def create_domination_chart():
    plt = setup_polish_matplotlib()
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_compare_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} porównań z ankiety compare")
    
    # Analiza dominacji - kto wybrał ten sam styl wszędzie
    domination_counts = {v: 0 for v in versions}
    domination_counts["mixed"] = 0  # Różne style w różnych kategoriach
    
    for entry in data:
        choices = [entry.get(cat) for cat in COMPARE_CATEGORIES]
        
        # Sprawdź czy wszystkie wybory są takie same
        unique_choices = set(c for c in choices if c is not None)
        
        if len(unique_choices) == 1:
            # Pełna dominacja jednego stylu
            dominant = list(unique_choices)[0]
            if dominant in versions:
                domination_counts[dominant] += 1
        else:
            # Mieszane wybory
            domination_counts["mixed"] += 1
    
    total = len(data)
    
    # ===== WYKRES 1: Pie chart dominacji =====
    fig, ax = plt.subplots(figsize=(11, 8))
    
    # Przygotuj dane
    labels_list = versions + ["mixed"]
    values = [domination_counts[v] for v in labels_list]
    
    # Kolory
    colors = [VERSION_COLORS[v] for v in versions] + ["#9E9E9E"]  # Szary dla mixed
    
    # Etykiety
    display_labels = [VERSION_LABELS[v] for v in versions] + ["Różne wybory"]
    
    # Wyróżnij zwycięzcę (bez mixed)
    version_values = [domination_counts[v] for v in versions]
    if max(version_values) > 0:
        max_idx = version_values.index(max(version_values))
        explode = [0.05 if i == max_idx else 0 for i in range(len(versions))] + [0]
    else:
        explode = [0] * len(labels_list)
    
    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=colors, autopct='',
        explode=explode, startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 2}
    )
    
    ax.set_title(f'Analiza dominacji - spójność wyborów\n(n={total} respondentów)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Legenda po prawej stronie z wartościami
    legend_labels = []
    for i, label in enumerate(display_labels):
        count = values[i]
        pct = (count / total * 100) if total > 0 else 0
        legend_labels.append(f"{label}: {count} ({pct:.1f}%)")
    
    legend_colors = colors
    legend_elements = [Patch(facecolor=c, edgecolor='black', label=l) 
                      for c, l in zip(legend_colors, legend_labels)]
    ax.legend(handles=legend_elements, title='Wybór we wszystkich\nkategoriach', 
              loc='upper right', bbox_to_anchor=(1.45, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "compare_domination")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - ANALIZA DOMINACJI")
    print("="*60)
    
    print(f"\nRozkład dominacji (n={total}):")
    for version in versions:
        count = domination_counts[version]
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {VERSION_LABELS[version]} wszędzie: {count} ({pct:.1f}%)")
    
    print(f"  Różne wybory: {domination_counts['mixed']} ({domination_counts['mixed']/total*100:.1f}%)")
    
    full_dom = sum(domination_counts[v] for v in versions)
    print(f"\n📊 Pełna dominacja (jakikolwiek styl): {full_dom} ({full_dom/total*100:.1f}%)")
    print(f"📊 Zróżnicowane wybory: {domination_counts['mixed']} ({domination_counts['mixed']/total*100:.1f}%)")


if __name__ == "__main__":
    create_domination_chart()

