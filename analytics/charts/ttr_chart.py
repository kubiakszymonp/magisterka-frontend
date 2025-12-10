"""
Wykres: Type-Token Ratio (TTR) - Bogactwo słownictwa

OPIS WYKRESU:
TTR mierzy stosunek unikalnych słów (typów) do wszystkich słów (tokenów).
Wyższy TTR = większa różnorodność słownictwa.

Analizujemy dwie wersje:
- ttr_tokens: na podstawie form słów (jak w tekście)
- ttr_lemmas: na podstawie lemmatów (form podstawowych)

CO PORÓWNUJE:
- Bogactwo słownictwa między wersjami tekstów
- Różnicę między analizą tokenów vs lemmatów

INTERPRETACJA:
- TTR 0.5-0.7 = typowy zakres dla tekstów
- Wyższy TTR = bardziej zróżnicowane słownictwo
- TTR lemmas jest zwykle niższy (różne formy → ten sam lemat)
- Dłuższe teksty mają zwykle niższy TTR (więcej powtórzeń)
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


def create_ttr_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("ttr")["data"]
    
    # Agreguj według wersji
    ttr_tokens_by_version = aggregate_by_version(raw_data, "ttr_tokens")
    ttr_lemmas_by_version = aggregate_by_version(raw_data, "ttr_lemmas")
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: TTR tokeny =====
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(versions))
    width = 0.6
    labels = [VERSION_LABELS[v] for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    means_tokens = [np.mean(ttr_tokens_by_version[v]) for v in versions]
    stds_tokens = [np.std(ttr_tokens_by_version[v]) for v in versions]
    
    bars1 = ax1.bar(x, means_tokens, width, yerr=stds_tokens, 
                   color=colors, edgecolor='black', linewidth=1.2,
                   capsize=5, error_kw={'linewidth': 2, 'capthick': 2})
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Type-Token Ratio (tokeny)', fontsize=12, fontweight='bold')
    ax1.set_title('Bogactwo słownictwa: TTR tokeny\n(wyższy = bardziej zróżnicowane słownictwo, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_ylim(0.35, 0.85)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax1.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # Dodaj wartości
    for bar, mean in zip(bars1, means_tokens):
        ax1.annotate(f'{mean:.3f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "ttr_tokens")
    plt.close(fig1)
    
    # ===== WYKRES 2: TTR lematy =====
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    means_lemmas = [np.mean(ttr_lemmas_by_version[v]) for v in versions]
    stds_lemmas = [np.std(ttr_lemmas_by_version[v]) for v in versions]
    
    bars2 = ax2.bar(x, means_lemmas, width, yerr=stds_lemmas,
                   color=colors, edgecolor='black', linewidth=1.2,
                   capsize=5, error_kw={'linewidth': 2, 'capthick': 2})
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Type-Token Ratio (lematy)', fontsize=12, fontweight='bold')
    ax2.set_title('Bogactwo słownictwa: TTR lematy\n(wyższy = bardziej zróżnicowane słownictwo, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.set_ylim(0.35, 0.85)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax2.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # Dodaj wartości
    for bar, mean in zip(bars2, means_lemmas):
        ax2.annotate(f'{mean:.3f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig2, "ttr_lemmas")
    plt.close(fig2)
    
    # ===== WYKRES 3: Radar/Spider chart dla TTR tokenów =====
    fig3, ax3 = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    categories = labels
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Zamknij wykres
    
    for metric_name, metric_data, color, label in [
        ('ttr_tokens', ttr_tokens_by_version, '#3498db', 'TTR (tokeny)'),
        ('ttr_lemmas', ttr_lemmas_by_version, '#e74c3c', 'TTR (lematy)')
    ]:
        values = [np.mean(metric_data[v]) for v in versions]
        values += values[:1]
        ax3.plot(angles, values, 'o-', linewidth=2, label=label, color=color)
        ax3.fill(angles, values, alpha=0.25, color=color)
    
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(categories)
    ax3.set_ylim(0.4, 0.75)
    ax3.set_title('Porównanie TTR między wersjami (wykres radarowy)', y=1.08, fontsize=14, fontweight='bold')
    ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), title='Typ analizy', framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig3, "ttr_radar")
    plt.close(fig3)
    
    # ===== WYKRES 4: Boxplot TTR tokeny =====
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    
    colors = [VERSION_COLORS[v] for v in versions]
    
    # TTR tokens
    tokens_data = [ttr_tokens_by_version[v] for v in versions]
    bp1 = ax4.boxplot(tokens_data, labels=labels, patch_artist=True,
                      medianprops={'color': 'black', 'linewidth': 2})
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax4.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax4.set_ylabel('TTR (tokeny)', fontsize=12, fontweight='bold')
    ax4.set_title('Rozkład TTR dla tokenów (boxplot)', fontsize=14, fontweight='bold', pad=15)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax4.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig4, "ttr_tokens_boxplot")
    plt.close(fig4)
    
    # ===== WYKRES 5: Boxplot TTR lematy =====
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    
    # TTR lemmas
    lemmas_data = [ttr_lemmas_by_version[v] for v in versions]
    bp2 = ax5.boxplot(lemmas_data, labels=labels, patch_artist=True,
                      medianprops={'color': 'black', 'linewidth': 2})
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax5.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax5.set_ylabel('TTR (lematy)', fontsize=12, fontweight='bold')
    ax5.set_title('Rozkład TTR dla lemmatów (boxplot)', fontsize=14, fontweight='bold', pad=15)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax5.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig5, "ttr_lemmas_boxplot")
    plt.close(fig5)
    
    # ===== WYKRES 6: Scatter - związek TTR tokens vs lemmas =====
    fig6, ax6 = plt.subplots(figsize=(10, 8))
    
    for version in versions:
        ax6.scatter(ttr_tokens_by_version[version], ttr_lemmas_by_version[version],
                   c=VERSION_COLORS[version], label=VERSION_LABELS[version],
                   s=100, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Linia y=x jako odniesienie
    ax6.plot([0.4, 0.8], [0.4, 0.8], 'k--', alpha=0.3, label='y = x')
    
    ax6.set_xlabel('TTR (tokeny)', fontsize=12, fontweight='bold')
    ax6.set_ylabel('TTR (lematy)', fontsize=12, fontweight='bold')
    ax6.set_title('Korelacja między TTR tokenów a lemmatów\n(punkty poniżej linii = lematyzacja redukuje liczbę unikalnych form, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax6.legend(title='Wersja tekstu', loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    ax6.set_xlim(0.45, 0.8)
    ax6.set_ylim(0.35, 0.75)
    
    plt.tight_layout()
    save_chart(fig6, "ttr_correlation")
    plt.close(fig6)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - TYPE-TOKEN RATIO")
    print("="*60)
    for v in versions:
        print(f"\n{VERSION_LABELS[v]}:")
        stats_tokens = calculate_stats(ttr_tokens_by_version[v])
        stats_lemmas = calculate_stats(ttr_lemmas_by_version[v])
        print(f"  TTR tokens: {stats_tokens['mean']:.4f} ± {stats_tokens['std']:.4f}")
        print(f"  TTR lemmas: {stats_lemmas['mean']:.4f} ± {stats_lemmas['std']:.4f}")
        print(f"  Redukcja przez lematyzację: {(1 - stats_lemmas['mean']/stats_tokens['mean'])*100:.1f}%")


if __name__ == "__main__":
    create_ttr_charts()

