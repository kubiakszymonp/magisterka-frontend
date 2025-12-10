"""
Wykres: MTLD (Measure of Textual Lexical Diversity)

OPIS WYKRESU:
MTLD to zaawansowana miara różnorodności leksykalnej, która jest mniej
wrażliwa na długość tekstu niż prosty TTR. Wyższy MTLD = bardziej
zróżnicowane słownictwo.

Analizujemy:
- mtld_tokens: na podstawie form słów
- mtld_lemmas: na podstawie lemmatów

CO PORÓWNUJE:
- Różnorodność leksykalną między wersjami
- Stabilność miary niezależnie od długości tekstu

INTERPRETACJA:
- MTLD > 100 = akceptowalna różnorodność
- MTLD > 200 = dobra różnorodność
- W przeciwieństwie do TTR, MTLD jest stabilne dla różnych długości tekstu
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_aggregated_data, aggregate_by_version, calculate_stats,
    setup_polish_matplotlib, save_chart, get_ordered_versions,
    VERSION_LABELS, VERSION_COLORS
)
import numpy as np


def create_mtld_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("mtld")["data"]
    
    # Agreguj według wersji
    mtld_tokens_by_version = aggregate_by_version(raw_data, "mtld_tokens")
    mtld_lemmas_by_version = aggregate_by_version(raw_data, "mtld_lemmas")
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: MTLD tokeny =====
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(versions))
    width = 0.6
    labels = [VERSION_LABELS[v] for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    means_tokens = [np.mean(mtld_tokens_by_version[v]) for v in versions]
    stds_tokens = [np.std(mtld_tokens_by_version[v]) for v in versions]
    
    bars1 = ax1.bar(x, means_tokens, width, yerr=stds_tokens,
                   color=colors, edgecolor='black', linewidth=1.2,
                   capsize=5, error_kw={'linewidth': 2, 'capthick': 2})
    
    # Linie referencyjne
    ax1.axhline(y=100, color='orange', linestyle='--', alpha=0.5, label='Akceptowalne (100)')
    ax1.axhline(y=200, color='green', linestyle='--', alpha=0.5, label='Dobre (200)')
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('MTLD (tokeny)', fontsize=12, fontweight='bold')
    ax1.set_title('Różnorodność leksykalna MTLD - tokeny\n(wyższy = bardziej zróżnicowane słownictwo, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    from matplotlib.lines import Line2D
    legend_elements.extend([
        Line2D([0], [0], color='orange', linestyle='--', alpha=0.5, label='Akceptowalne (100)'),
        Line2D([0], [0], color='green', linestyle='--', alpha=0.5, label='Dobre (200)')
    ])
    ax1.legend(handles=legend_elements, title='Wersja tekstu / Poziomy', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # Dodaj wartości
    for bar, mean in zip(bars1, means_tokens):
        ax1.annotate(f'{mean:.0f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "mtld_tokens")
    plt.close(fig1)
    
    # ===== WYKRES 2: MTLD lematy =====
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    means_lemmas = [np.mean(mtld_lemmas_by_version[v]) for v in versions]
    stds_lemmas = [np.std(mtld_lemmas_by_version[v]) for v in versions]
    
    bars2 = ax2.bar(x, means_lemmas, width, yerr=stds_lemmas,
                   color=colors, edgecolor='black', linewidth=1.2,
                   capsize=5, error_kw={'linewidth': 2, 'capthick': 2})
    
    # Linie referencyjne
    ax2.axhline(y=100, color='orange', linestyle='--', alpha=0.5, label='Akceptowalne (100)')
    ax2.axhline(y=200, color='green', linestyle='--', alpha=0.5, label='Dobre (200)')
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('MTLD (lematy)', fontsize=12, fontweight='bold')
    ax2.set_title('Różnorodność leksykalna MTLD - lematy\n(wyższy = bardziej zróżnicowane słownictwo, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    from matplotlib.lines import Line2D
    legend_elements.extend([
        Line2D([0], [0], color='orange', linestyle='--', alpha=0.5, label='Akceptowalne (100)'),
        Line2D([0], [0], color='green', linestyle='--', alpha=0.5, label='Dobre (200)')
    ])
    ax2.legend(handles=legend_elements, title='Wersja tekstu / Poziomy', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # Dodaj wartości
    for bar, mean in zip(bars2, means_lemmas):
        ax2.annotate(f'{mean:.0f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig2, "mtld_lemmas")
    plt.close(fig2)
    
    # ===== WYKRES 3: Boxplot MTLD tokeny =====
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    
    colors = [VERSION_COLORS[v] for v in versions]
    
    # MTLD tokens
    tokens_data = [mtld_tokens_by_version[v] for v in versions]
    bp1 = ax3.boxplot(tokens_data, labels=labels, patch_artist=True,
                      medianprops={'color': 'black', 'linewidth': 2},
                      widths=0.6)
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Dodaj punkty
    for i, (version, data) in enumerate(zip(versions, tokens_data)):
        jitter = np.random.normal(0, 0.04, len(data))
        ax3.scatter(np.ones(len(data)) * (i + 1) + jitter, data,
                   c='black', alpha=0.4, s=20, zorder=3)
    
    ax3.axhline(y=200, color='green', linestyle='--', alpha=0.5, label='Dobra różnorodność (200)')
    ax3.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax3.set_ylabel('MTLD (tokeny)', fontsize=12, fontweight='bold')
    ax3.set_title('Rozkład MTLD dla tokenów (boxplot)', fontsize=14, fontweight='bold', pad=15)
    
    # Legenda
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    legend_elements.append(Line2D([0], [0], color='green', linestyle='--', alpha=0.5, label='Dobra różnorodność (200)'))
    ax3.legend(handles=legend_elements, title='Legenda', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig3, "mtld_tokens_boxplot")
    plt.close(fig3)
    
    # ===== WYKRES 4: Boxplot MTLD lematy =====
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    
    # MTLD lemmas
    lemmas_data = [mtld_lemmas_by_version[v] for v in versions]
    bp2 = ax4.boxplot(lemmas_data, labels=labels, patch_artist=True,
                      medianprops={'color': 'black', 'linewidth': 2},
                      widths=0.6)
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    for i, (version, data) in enumerate(zip(versions, lemmas_data)):
        jitter = np.random.normal(0, 0.04, len(data))
        ax4.scatter(np.ones(len(data)) * (i + 1) + jitter, data,
                   c='black', alpha=0.4, s=20, zorder=3)
    
    ax4.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax4.set_ylabel('MTLD (lematy)', fontsize=12, fontweight='bold')
    ax4.set_title('Rozkład MTLD dla lemmatów (boxplot)', fontsize=14, fontweight='bold', pad=15)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax4.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig4, "mtld_lemmas_boxplot")
    plt.close(fig4)
    
    # ===== WYKRES 5: MTLD vs długość tekstu (z word_count) =====
    fig5, ax5 = plt.subplots(figsize=(10, 8))
    
    # Wczytaj też word_count
    word_count_data = load_aggregated_data("word_count")["data"]
    
    for version in versions:
        mtld_values = []
        word_counts = []
        for article in raw_data.keys():
            if version in raw_data[article] and version in word_count_data.get(article, {}):
                mtld_values.append(raw_data[article][version]["mtld_tokens"])
                word_counts.append(word_count_data[article][version])
        
        ax5.scatter(word_counts, mtld_values, c=VERSION_COLORS[version],
                   label=VERSION_LABELS[version], s=80, alpha=0.7,
                   edgecolors='black', linewidth=1)
    
    ax5.set_xlabel('Liczba słów w tekście', fontsize=12, fontweight='bold')
    ax5.set_ylabel('MTLD (tokeny)', fontsize=12, fontweight='bold')
    ax5.set_title('MTLD vs długość tekstu\n(MTLD powinno być stabilne niezależnie od długości, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax5.legend(title='Wersja tekstu', loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig5, "mtld_vs_length")
    plt.close(fig5)
    
    # ===== WYKRES 6: Violin plot =====
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    
    # Przygotuj dane w formacie dla seaborn
    import pandas as pd
    
    plot_data = []
    for version in versions:
        for val in mtld_tokens_by_version[version]:
            plot_data.append({
                'Wersja': VERSION_LABELS[version],
                'MTLD': val,
                'Typ': 'Tokeny'
            })
        for val in mtld_lemmas_by_version[version]:
            plot_data.append({
                'Wersja': VERSION_LABELS[version],
                'MTLD': val,
                'Typ': 'Lematy'
            })
    
    df = pd.DataFrame(plot_data)
    
    sns.violinplot(data=df, x='Wersja', y='MTLD', hue='Typ', split=True, ax=ax6,
                   palette=['#9b59b6', '#1abc9c'], alpha=0.8)
    
    ax6.set_title('Rozkład MTLD: tokeny vs lematy (violin plot)', fontsize=14, fontweight='bold', pad=15)
    ax6.axhline(y=200, color='green', linestyle='--', alpha=0.5, label='Dobra różnorodność (200)')
    ax6.legend(loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=9)
    
    plt.tight_layout()
    save_chart(fig6, "mtld_violin")
    plt.close(fig6)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - MTLD")
    print("="*60)
    for v in versions:
        print(f"\n{VERSION_LABELS[v]}:")
        stats_tokens = calculate_stats(mtld_tokens_by_version[v])
        stats_lemmas = calculate_stats(mtld_lemmas_by_version[v])
        print(f"  MTLD tokens: {stats_tokens['mean']:.1f} ± {stats_tokens['std']:.1f}")
        print(f"  MTLD lemmas: {stats_lemmas['mean']:.1f} ± {stats_lemmas['std']:.1f}")


if __name__ == "__main__":
    create_mtld_charts()

