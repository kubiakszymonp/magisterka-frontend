"""
Wykres: TF-IDF Overlap - Pokrywanie się kluczowych terminów

OPIS WYKRESU:
TF-IDF (Term Frequency-Inverse Document Frequency) identyfikuje najważniejsze
słowa w tekście. Ten wykres pokazuje, ile z top-N najważniejszych terminów
jest wspólnych między wersjami tekstu.

Wartości wyrażone w procentach (0-100%):
- 100% = wszystkie kluczowe terminy są wspólne
- 0% = brak wspólnych kluczowych terminów

CO PORÓWNUJE:
- Czy różne wersje zachowują te same kluczowe pojęcia
- Podobieństwo tematyczne między wersjami

INTERPRETACJA:
- Wysoki overlap = wersje skupiają się na tych samych aspektach tematu
- Niski overlap = różne wersje podkreślają różne aspekty
- Oczekujemy wyższego overlap dla wersji dla tego samego odbiorcy
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_aggregated_data, aggregate_pairs, calculate_stats,
    setup_polish_matplotlib, save_chart, get_ordered_pairs,
    PAIR_LABELS, PAIR_COLORS
)
import numpy as np


def create_tfidf_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("tfidf_overlap")["data"]
    
    # Agreguj według par
    by_pair = aggregate_pairs(raw_data)
    pairs = get_ordered_pairs()
    
    # ===== WYKRES 1: Bar chart =====
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(pairs))
    width = 0.6
    labels = [PAIR_LABELS[p] for p in pairs]
    colors = [PAIR_COLORS[p] for p in pairs]
    
    means = [np.mean(by_pair[p]) for p in pairs]
    stds = [np.std(by_pair[p]) for p in pairs]
    
    bars = ax1.bar(x, means, width, yerr=stds, capsize=5,
                  color=colors, edgecolor='black', linewidth=1.2,
                  error_kw={'linewidth': 2, 'capthick': 2})
    
    # Linie referencyjne
    ax1.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label='50% overlap')
    ax1.axhline(y=70, color='green', linestyle='--', alpha=0.5, label='70% overlap (wysoki)')
    
    ax1.set_xlabel('Para porównywanych wersji', fontsize=12, fontweight='bold')
    ax1.set_ylabel('TF-IDF Overlap (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Pokrywanie się kluczowych terminów (TF-IDF)\n(wyższy = więcej wspólnych ważnych pojęć, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=10, ha='right')
    ax1.set_ylim(0, 100)
    ax1.legend(loc='lower left', bbox_to_anchor=(1.02, 0), title='Poziomy overlap', framealpha=0.9, fontsize=9)
    
    # Legenda kolorów par
    from matplotlib.patches import Patch
    pair_legend = [Patch(facecolor=PAIR_COLORS[p], edgecolor='black', label=PAIR_LABELS[p]) 
                    for p in pairs]
    ax1.legend(handles=pair_legend + ax1.get_legend().get_patches(), 
               title='Para wersji / Poziomy', loc='lower left', bbox_to_anchor=(1.02, 0), framealpha=0.9, fontsize=9)
    
    for bar, mean, std in zip(bars, means, stds):
        ax1.annotate(f'{mean:.0f}%',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "tfidf_bar")
    
    # ===== WYKRES 2: Boxplot =====
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    plot_data = [by_pair[p] for p in pairs]
    
    bp = ax2.boxplot(plot_data, labels=labels, patch_artist=True,
                     medianprops={'color': 'black', 'linewidth': 2},
                     widths=0.6)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Dodaj punkty
    for i, (pair, vals) in enumerate(zip(pairs, plot_data)):
        jitter = np.random.normal(0, 0.04, len(vals))
        ax2.scatter(np.ones(len(vals)) * (i + 1) + jitter, vals,
                   c='black', alpha=0.4, s=25, zorder=3)
    
    ax2.axhline(y=50, color='orange', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Para wersji', fontsize=12, fontweight='bold')
    ax2.set_ylabel('TF-IDF Overlap (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Rozkład pokrywania się kluczowych terminów (boxplot)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticklabels(labels, rotation=10, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=PAIR_COLORS[p], edgecolor='black', alpha=0.7, label=PAIR_LABELS[p]) 
                       for p in pairs]
    from matplotlib.lines import Line2D
    legend_elements.append(Line2D([0], [0], color='orange', linestyle='--', alpha=0.5, label='50% overlap'))
    ax2.legend(handles=legend_elements, title='Legenda', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig2, "tfidf_boxplot")
    
    # ===== WYKRES 3: Heatmapa =====
    fig3, ax3 = plt.subplots(figsize=(9, 7))
    
    versions = ["child_short", "adult_short", "adult_full"]
    version_labels = ["Dziecięca", "Dorosła (krótka)", "Dorosła (pełna)"]
    
    overlap_matrix = np.ones((3, 3)) * 100
    
    pair_to_indices = {
        "adult_full__adult_short": (2, 1),
        "adult_full__child_short": (2, 0),
        "adult_short__child_short": (1, 0)
    }
    
    for pair, (i, j) in pair_to_indices.items():
        mean_val = np.mean(by_pair[pair])
        overlap_matrix[i, j] = mean_val
        overlap_matrix[j, i] = mean_val
    
    im = ax3.imshow(overlap_matrix, cmap='Greens', vmin=40, vmax=100)
    
    ax3.set_xticks(range(3))
    ax3.set_yticks(range(3))
    ax3.set_xticklabels(version_labels, rotation=30, ha='right')
    ax3.set_yticklabels(version_labels)
    
    for i in range(3):
        for j in range(3):
            color = 'white' if overlap_matrix[i, j] > 70 else 'black'
            ax3.text(j, i, f'{overlap_matrix[i, j]:.0f}%',
                    ha='center', va='center', color=color, fontsize=12, fontweight='bold')
    
    ax3.set_title('Macierz TF-IDF Overlap\n(średnie dla wszystkich artykułów, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    plt.colorbar(im, ax=ax3, label='Overlap (%)')
    
    plt.tight_layout()
    save_chart(fig3, "tfidf_heatmap")
    
    # ===== WYKRES 4: Porównanie z Jaccarda =====
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    # Wczytaj też Jaccard
    jaccard_data = load_aggregated_data("jaccard_similarity")["data"]
    jaccard_by_pair = aggregate_pairs(jaccard_data)
    
    x = np.arange(len(pairs))
    width = 0.35
    
    tfidf_means = [np.mean(by_pair[p]) for p in pairs]
    jaccard_means = [np.mean(jaccard_by_pair[p]) * 100 for p in pairs]  # Skaluj do %
    
    bars1 = ax4.bar(x - width/2, tfidf_means, width, label='TF-IDF Overlap',
                   color='#2ecc71', edgecolor='black')
    bars2 = ax4.bar(x + width/2, jaccard_means, width, label='Jaccard × 100',
                   color='#3498db', edgecolor='black')
    
    ax4.set_xlabel('Para wersji', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Wartość (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Porównanie TF-IDF Overlap vs Jaccard Similarity\n(Jaccard przeskalowany ×100 dla porównania, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels, rotation=10, ha='right')
    ax4.legend(title='Metryka', loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # Wartości
    for bars, means in [(bars1, tfidf_means), (bars2, jaccard_means)]:
        for bar, mean in zip(bars, means):
            ax4.annotate(f'{mean:.0f}',
                        xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig4, "tfidf_vs_jaccard")
    
    # ===== WYKRES 5: Scatter per artykuł =====
    fig5, ax5 = plt.subplots(figsize=(10, 8))
    
    for pair in pairs:
        tfidf_vals = []
        jaccard_vals = []
        for article in raw_data.keys():
            if pair in raw_data[article] and pair in jaccard_data.get(article, {}):
                tfidf_vals.append(raw_data[article][pair])
                jaccard_vals.append(jaccard_data[article][pair] * 100)
        
        ax5.scatter(jaccard_vals, tfidf_vals, c=PAIR_COLORS[pair],
                   label=PAIR_LABELS[pair], s=80, alpha=0.7,
                   edgecolors='black', linewidth=1)
    
    ax5.set_xlabel('Jaccard Similarity × 100', fontsize=12, fontweight='bold')
    ax5.set_ylabel('TF-IDF Overlap (%)', fontsize=12, fontweight='bold')
    ax5.set_title('Korelacja: TF-IDF Overlap vs Jaccard Similarity\n(n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax5.legend(title='Para wersji', loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig5, "tfidf_jaccard_correlation")
    plt.close(fig5)
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    plt.close(fig4)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - TF-IDF OVERLAP")
    print("="*60)
    for p in pairs:
        print(f"\n{PAIR_LABELS[p]}:")
        stats = calculate_stats(by_pair[p])
        print(f"  Średnia: {stats['mean']:.1f}% ± {stats['std']:.1f}%")
        print(f"  Mediana: {stats['median']:.1f}%")
        print(f"  Zakres: {stats['min']:.1f}% - {stats['max']:.1f}%")


if __name__ == "__main__":
    create_tfidf_charts()

