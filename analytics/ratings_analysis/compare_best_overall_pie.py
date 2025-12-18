"""
Wykres #8: Pie chart / Donut chart - bestOverall

OPIS WYKRESU:
Wykres kołowy pokazujący rozkład odpowiedzi na pytanie
"Która wersja artykułu jest najlepsza ogólnie?"

CO PORÓWNUJE:
- Ogólną preferencję użytkowników
- Który typ artykułu jest najczęściej wybierany jako najlepszy

INTERPRETACJA:
- Większy wycinek = więcej głosów
- Pokazuje "zwycięzcę" w kategorii ogólnej
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_compare_ratings, count_compare_wins, setup_polish_matplotlib, save_chart,
    get_ordered_versions, VERSION_LABELS, VERSION_COLORS
)
import numpy as np


def create_best_overall_pie_chart():
    plt = setup_polish_matplotlib()
    
    # Wczytaj dane
    data = load_compare_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} porównań z ankiety compare")
    
    # Zlicz zwycięstwa dla bestOverall
    wins = count_compare_wins(data, "bestOverall")
    total = sum(wins.values())
    
    # ===== WYKRES 1: Pie chart =====
    fig, ax = plt.subplots(figsize=(10, 8))
    
    values = [wins[v] for v in versions]
    labels = [f"{VERSION_LABELS[v]}\n{wins[v]} ({wins[v]/total*100:.1f}%)" for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    # Wyróżnij zwycięzcę
    max_idx = values.index(max(values))
    explode = [0.05 if i == max_idx else 0 for i in range(len(versions))]
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors,
                                       autopct='', explode=explode,
                                       startangle=90, 
                                       wedgeprops={'edgecolor': 'black', 'linewidth': 2})
    
    ax.set_title(f'Najlepsza wersja artykułu ogólnie\n(n={total} porównań)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Legenda po prawej stronie
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', 
                            label=f"{VERSION_LABELS[v]}: {wins[v]} ({wins[v]/total*100:.1f}%)") 
                      for v in versions]
    ax.legend(handles=legend_elements, title='Typ artykułu', 
              loc='upper left', bbox_to_anchor=(1.02, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "compare_best_overall_pie")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - NAJLEPSZA WERSJA OGÓLNIE")
    print("="*60)
    
    print(f"\nRozkład odpowiedzi (n={total}):")
    for version in versions:
        count = wins[version]
        pct = (count / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  {VERSION_LABELS[version]}: {count:3d} ({pct:5.1f}%) {bar}")
    
    # Zwycięzca
    winner = max(wins, key=wins.get)
    print(f"\n🏆 Zwycięzca: {VERSION_LABELS[winner]} ({wins[winner]} głosów)")


if __name__ == "__main__":
    create_best_overall_pie_chart()

