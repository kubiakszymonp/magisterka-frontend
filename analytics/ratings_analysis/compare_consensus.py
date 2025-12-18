"""
Wykres C-C: Konsensus per kategoria

OPIS WYKRESU:
Bar chart pokazujący procent respondentów którzy wybrali "zwycięzcę"
(najczęściej wybierany styl) w każdej kategorii.

CO PORÓWNUJE:
- W której kategorii jest największa zgodność
- W której kategorii opinie są najbardziej podzielone

INTERPRETACJA:
- Wysoki % = duży konsensus (jeden styl wyraźnie wygrywa)
- Niski % = opinie podzielone (różne style mają podobne wyniki)
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


def create_consensus_chart():
    plt = setup_polish_matplotlib()
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_compare_ratings()
    versions = get_ordered_versions()
    total = len(data)
    
    print(f"Wczytano {len(data)} porównań z ankiety compare")
    
    # Dla każdej kategorii znajdź zwycięzcę i oblicz konsensus
    consensus_data = []
    
    for category in COMPARE_CATEGORIES:
        wins = count_compare_wins(data, category)
        
        # Zwycięzca
        winner = max(wins, key=wins.get)
        winner_count = wins[winner]
        winner_pct = (winner_count / total * 100) if total > 0 else 0
        
        # Drugi w kolejności
        sorted_wins = sorted(wins.items(), key=lambda x: x[1], reverse=True)
        runner_up = sorted_wins[1][0] if len(sorted_wins) > 1 else None
        runner_up_count = sorted_wins[1][1] if len(sorted_wins) > 1 else 0
        runner_up_pct = (runner_up_count / total * 100) if total > 0 else 0
        
        consensus_data.append({
            "category": category,
            "winner": winner,
            "winner_count": winner_count,
            "winner_pct": winner_pct,
            "runner_up": runner_up,
            "runner_up_count": runner_up_count,
            "runner_up_pct": runner_up_pct,
            "margin": winner_pct - runner_up_pct
        })
    
    # Sortuj według konsensusu (malejąco)
    consensus_data.sort(key=lambda x: x["winner_pct"], reverse=True)
    
    # ===== WYKRES 1: Bar chart konsensusu =====
    fig, ax = plt.subplots(figsize=(14, 8))
    
    categories = [d["category"] for d in consensus_data]
    consensus_pcts = [d["winner_pct"] for d in consensus_data]
    winners = [d["winner"] for d in consensus_data]
    colors = [VERSION_COLORS[w] for w in winners]
    
    x = np.arange(len(categories))
    bars = ax.bar(x, consensus_pcts, 0.6, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Kategoria porównania', fontsize=12, fontweight='bold')
    ax.set_ylabel('Konsensus (% dla zwycięzcy)', fontsize=12, fontweight='bold')
    ax.set_title(f'Siła konsensusu w każdej kategorii\n(% respondentów wybierających najpopularniejszy styl, n={total})', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([COMPARE_CATEGORY_LABELS[c] for c in categories], rotation=20, ha='right')
    ax.set_ylim(0, 100)
    
    # Linia 33% (równy podział między 3 style)
    ax.axhline(y=33.3, color='red', linestyle='--', alpha=0.7, label='Równy podział (33%)')
    ax.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label='Większość (50%)')
    
    # Wartości na słupkach
    for bar, d in zip(bars, consensus_data):
        ax.annotate(f'{d["winner_pct"]:.1f}%\n({VERSION_LABELS[d["winner"]].split()[0]})',
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   xytext=(0, 5), textcoords='offset points',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Legenda po prawej stronie
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', 
                            label=VERSION_LABELS[v]) for v in versions]
    legend_elements.extend([
        plt.Line2D([0], [0], color='red', linestyle='--', label='Równy podział (33%)'),
        plt.Line2D([0], [0], color='orange', linestyle='--', label='Większość (50%)')
    ])
    ax.legend(handles=legend_elements, title='Legenda', 
              loc='upper left', bbox_to_anchor=(1.02, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "compare_consensus")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - KONSENSUS PER KATEGORIA")
    print("="*60)
    
    print("\nRanking kategorii według siły konsensusu:")
    for i, d in enumerate(consensus_data, 1):
        print(f"\n{i}. {COMPARE_CATEGORY_LABELS[d['category']]}:")
        print(f"   🏆 Zwycięzca: {VERSION_LABELS[d['winner']]} ({d['winner_pct']:.1f}%)")
        print(f"   🥈 Drugi: {VERSION_LABELS[d['runner_up']]} ({d['runner_up_pct']:.1f}%)")
        print(f"   📊 Przewaga: +{d['margin']:.1f} punktów procentowych")
    
    # Podsumowanie
    avg_consensus = np.mean([d["winner_pct"] for d in consensus_data])
    print(f"\n📈 Średni konsensus: {avg_consensus:.1f}%")
    
    max_consensus = max(consensus_data, key=lambda x: x["winner_pct"])
    min_consensus = min(consensus_data, key=lambda x: x["winner_pct"])
    print(f"📈 Największy konsensus: {COMPARE_CATEGORY_LABELS[max_consensus['category']]} ({max_consensus['winner_pct']:.1f}%)")
    print(f"📉 Najmniejszy konsensus: {COMPARE_CATEGORY_LABELS[min_consensus['category']]} ({min_consensus['winner_pct']:.1f}%)")


if __name__ == "__main__":
    create_consensus_chart()

