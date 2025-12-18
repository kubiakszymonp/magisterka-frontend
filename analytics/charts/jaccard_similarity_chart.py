"""
Wykres: Podobieństwo Jaccarda (Jaccard Similarity)

OPIS WYKRESU:
Indeks Jaccarda mierzy podobieństwo zbiorów słów między wersjami tekstu.
J = |A ∩ B| / |A ∪ B|, gdzie A i B to zbiory unikalnych słów.

Wartości:
- 0 = brak wspólnych słów
- 1 = identyczne zbiory słów

CO PORÓWNUJE:
- Podobieństwo słownictwa między parami wersji:
  - adult_full ↔ adult_short
  - adult_full ↔ child_short  
  - adult_short ↔ child_short

INTERPRETACJA:
- Wyższe podobieństwo = więcej wspólnego słownictwa
- Niskie podobieństwo może wskazywać na różne podejście do tematu
- Wersje dla tego samego odbiorcy powinny być bardziej podobne
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


def create_jaccard_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("jaccard_similarity")["data"]
    
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
    
    ax1.set_xlabel('Para porównywanych wersji', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Indeks Jaccarda', fontsize=12, fontweight='bold')
    ax1.set_title('Podobieństwo słownictwa między wersjami tekstów\n(wyższy = więcej wspólnych słów, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=10, ha='right')
    ax1.set_ylim(0, 0.45)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=PAIR_COLORS[p], edgecolor='black', label=PAIR_LABELS[p]) 
                       for p in pairs]
    ax1.legend(handles=legend_elements, title='Para wersji', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    for bar, mean, std in zip(bars, means, stds):
        ax1.annotate(f'{mean:.3f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height() + std),
                    xytext=(0, 8), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "jaccard_bar")
    
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
    
    ax2.set_xlabel('Para wersji', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Indeks Jaccarda', fontsize=12, fontweight='bold')
    ax2.set_title('Rozkład podobieństwa Jaccarda między wersjami (boxplot)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticklabels(labels, rotation=10, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=PAIR_COLORS[p], edgecolor='black', alpha=0.7, label=PAIR_LABELS[p]) 
                       for p in pairs]
    ax2.legend(handles=legend_elements, title='Para wersji', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig2, "jaccard_boxplot")
    
    # ===== WYKRES 3: Heatmapa średnich podobieństw =====
    fig3, ax3 = plt.subplots(figsize=(9, 7))
    
    # Przygotuj macierz podobieństw
    versions = ["child_short", "adult_short", "adult_full"]
    version_labels = ["Dziecięca", "Dorosła (krótka)", "Dorosła (pełna)"]
    
    similarity_matrix = np.ones((3, 3))  # 1 na przekątnej
    
    # Mapowanie par na indeksy
    pair_to_indices = {
        "adult_full__adult_short": (2, 1),
        "adult_full__child_short": (2, 0),
        "adult_short__child_short": (1, 0)
    }
    
    for pair, (i, j) in pair_to_indices.items():
        mean_val = np.mean(by_pair[pair])
        similarity_matrix[i, j] = mean_val
        similarity_matrix[j, i] = mean_val
    
    im = ax3.imshow(similarity_matrix, cmap='YlOrRd', vmin=0.2, vmax=1.0)
    
    ax3.set_xticks(range(3))
    ax3.set_yticks(range(3))
    ax3.set_xticklabels(version_labels, rotation=30, ha='right')
    ax3.set_yticklabels(version_labels)
    
    # Dodaj wartości
    for i in range(3):
        for j in range(3):
            color = 'white' if similarity_matrix[i, j] > 0.6 else 'black'
            ax3.text(j, i, f'{similarity_matrix[i, j]:.3f}',
                    ha='center', va='center', color=color, fontsize=12, fontweight='bold')
    
    ax3.set_title('Macierz podobieństwa Jaccarda\n(średnie dla wszystkich artykułów, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    plt.colorbar(im, ax=ax3, label='Indeks Jaccarda')
    
    plt.tight_layout()
    save_chart(fig3, "jaccard_heatmap")
    
    # ===== WYKRES 4: Violin plot =====
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    import pandas as pd
    plot_data_df = []
    for pair in pairs:
        for val in by_pair[pair]:
            plot_data_df.append({
                'Para': PAIR_LABELS[pair],
                'Jaccard': val
            })
    
    df = pd.DataFrame(plot_data_df)
    
    palette = {PAIR_LABELS[p]: PAIR_COLORS[p] for p in pairs}
    sns.violinplot(data=df, x='Para', y='Jaccard', palette=palette, ax=ax4)
    
    ax4.set_xlabel('Para wersji', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Indeks Jaccarda', fontsize=12, fontweight='bold')
    ax4.set_title('Rozkład podobieństwa słownictwa (violin plot, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax4.set_xticklabels([PAIR_LABELS[p] for p in pairs], rotation=10, ha='right')
    
    plt.tight_layout()
    save_chart(fig4, "jaccard_violin")
    plt.close(fig4)
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - PODOBIEŃSTWO JACCARDA")
    print("="*60)
    for p in pairs:
        print(f"\n{PAIR_LABELS[p]}:")
        stats = calculate_stats(by_pair[p])
        print(f"  Średnia: {stats['mean']:.4f} ± {stats['std']:.4f}")
        print(f"  Mediana: {stats['median']:.4f}")
        print(f"  Zakres: {stats['min']:.4f} - {stats['max']:.4f}")


if __name__ == "__main__":
    create_jaccard_charts()

