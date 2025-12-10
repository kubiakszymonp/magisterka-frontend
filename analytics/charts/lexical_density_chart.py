"""
Wykres: Gęstość leksykalna (Lexical Density)

OPIS WYKRESU:
Gęstość leksykalna to stosunek słów znaczących (rzeczowniki, czasowniki,
przymiotniki, przysłówki) do wszystkich słów. Wyrażana w procentach.

CO PORÓWNUJE:
- Proporcję słów niosących znaczenie między wersjami
- "Informacyjność" tekstów

INTERPRETACJA:
- Typowy zakres: 40-60% dla tekstów pisanych
- Wyższa gęstość = więcej informacji, trudniejszy tekst
- Teksty dla dzieci mogą mieć niższą gęstość (więcej słów funkcyjnych)
- Teksty naukowe/specjalistyczne mają wyższą gęstość
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


def create_lexical_density_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("lexical_density")["data"]
    
    # Agreguj według wersji
    by_version = aggregate_by_version(raw_data)
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: Bar chart =====
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(versions))
    width = 0.6
    labels = [VERSION_LABELS[v] for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    means = [np.mean(by_version[v]) for v in versions]
    stds = [np.std(by_version[v]) for v in versions]
    
    bars = ax1.bar(x, means, width, yerr=stds, capsize=5,
                  color=colors, edgecolor='black', linewidth=1.2,
                  error_kw={'linewidth': 2, 'capthick': 2})
    
    # Linie referencyjne
    ax1.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label='Typowy poziom (50%)')
    ax1.axhline(y=60, color='red', linestyle='--', alpha=0.5, label='Wysoka gęstość (60%)')
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Gęstość leksykalna (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Gęstość leksykalna tekstów\n(procent słów niosących znaczenie, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_ylim(55, 75)
    ax1.legend(loc='lower right', bbox_to_anchor=(1.02, 0), title='Poziomy gęstości', framealpha=0.9, fontsize=9)
    
    # Legenda kolorów wersji
    from matplotlib.patches import Patch
    version_legend = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                      for v in versions]
    ax1.legend(handles=version_legend + ax1.get_legend().get_patches(), 
               title='Wersja tekstu / Poziomy', loc='lower left', bbox_to_anchor=(1.02, 0), framealpha=0.9, fontsize=9)
    
    for bar, mean, std in zip(bars, means, stds):
        ax1.annotate(f'{mean:.1f}%',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "lexical_density_bar")
    
    # ===== WYKRES 2: Boxplot =====
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    plot_data = [by_version[v] for v in versions]
    
    bp = ax2.boxplot(plot_data, labels=labels, patch_artist=True,
                     medianprops={'color': 'black', 'linewidth': 2},
                     widths=0.6)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Dodaj punkty
    for i, (version, vals) in enumerate(zip(versions, plot_data)):
        jitter = np.random.normal(0, 0.04, len(vals))
        ax2.scatter(np.ones(len(vals)) * (i + 1) + jitter, vals,
                   c='black', alpha=0.4, s=25, zorder=3)
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Gęstość leksykalna (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Rozkład gęstości leksykalnej (boxplot)', fontsize=14, fontweight='bold', pad=15)
    ax2.axhline(y=60, color='red', linestyle='--', alpha=0.5, label='Wysoka gęstość (60%)')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    from matplotlib.lines import Line2D
    legend_elements.append(Line2D([0], [0], color='red', linestyle='--', alpha=0.5, label='Wysoka gęstość (60%)'))
    ax2.legend(handles=legend_elements, title='Legenda', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig2, "lexical_density_boxplot")
    
    # ===== WYKRES 3: Histogram dla każdej wersji =====
    fig3, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    
    for ax, version in zip(axes, versions):
        ax.hist(by_version[version], bins=10, color=VERSION_COLORS[version],
               edgecolor='black', alpha=0.7)
        ax.axvline(np.mean(by_version[version]), color='red', linestyle='--',
                  linewidth=2, label=f'Średnia: {np.mean(by_version[version]):.1f}%')
        ax.set_xlabel('Gęstość leksykalna (%)')
        ax.set_ylabel('Liczba artykułów')
        ax.set_title(VERSION_LABELS[version])
        ax.legend()
    
    fig3.suptitle('Dystrybucja gęstości leksykalnej według wersji', fontsize=14, y=1.02)
    plt.tight_layout()
    save_chart(fig3, "lexical_density_histogram")
    
    # ===== WYKRES 4: Porównanie z innymi metrykami =====
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    
    # Wczytaj avg_word_length dla korelacji
    word_length_data = load_aggregated_data("avg_word_length")["data"]
    
    for version in versions:
        ld_values = []
        wl_values = []
        for article in raw_data.keys():
            if version in raw_data[article] and version in word_length_data.get(article, {}):
                ld_values.append(raw_data[article][version])
                wl_values.append(word_length_data[article][version])
        
        ax4.scatter(wl_values, ld_values, c=VERSION_COLORS[version],
                   label=VERSION_LABELS[version], s=80, alpha=0.7,
                   edgecolors='black', linewidth=1)
    
    ax4.set_xlabel('Średnia długość słowa (znaki)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Gęstość leksykalna (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Korelacja: gęstość leksykalna vs długość słów\n(dłuższe słowa często = więcej słów znaczących, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax4.legend(title='Wersja tekstu', loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig4, "lexical_density_vs_word_length")
    plt.close(fig4)
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - GĘSTOŚĆ LEKSYKALNA")
    print("="*60)
    for v in versions:
        print(f"\n{VERSION_LABELS[v]}:")
        stats = calculate_stats(by_version[v])
        print(f"  Średnia: {stats['mean']:.1f}% ± {stats['std']:.1f}%")
        print(f"  Mediana: {stats['median']:.1f}%")
        print(f"  Zakres: {stats['min']:.1f}% - {stats['max']:.1f}%")


if __name__ == "__main__":
    create_lexical_density_charts()

