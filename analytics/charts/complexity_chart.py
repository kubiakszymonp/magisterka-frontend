"""
Wykres: Złożoność tekstu (średnia długość słów i zdań)

OPIS WYKRESU:
Analizuje złożoność lingwistyczną tekstów poprzez średnią długość słów
i zdań. Te metryki są kluczowe dla oceny trudności tekstu.

CO PORÓWNUJE:
- Średnią długość słów (w znakach) - wskaźnik złożoności słownictwa
- Średnią długość zdań (w słowach) - wskaźnik złożoności składniowej

INTERPRETACJA:
- Dłuższe słowa = bardziej specjalistyczne/złożone słownictwo
- Dłuższe zdania = bardziej złożona składnia
- Teksty dla dzieci powinny mieć krótsze słowa i zdania
- Wersje dla dorosłych mogą zawierać dłuższe, bardziej złożone konstrukcje
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


def create_complexity_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    word_length_data = load_aggregated_data("avg_word_length")["data"]
    sentence_length_data = load_aggregated_data("avg_sentence_length")["data"]
    
    # Agreguj według wersji
    word_len_by_version = aggregate_by_version(word_length_data)
    sent_len_by_version = aggregate_by_version(sentence_length_data)
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: Porównanie obu metryk =====
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x = np.arange(len(versions))
    width = 0.6
    labels = [VERSION_LABELS[v] for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    # Lewy wykres - długość słów
    means_word = [np.mean(word_len_by_version[v]) for v in versions]
    stds_word = [np.std(word_len_by_version[v]) for v in versions]
    
    bars1 = ax1.bar(x, means_word, width, yerr=stds_word, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Średnia długość słowa (znaki)', fontsize=12, fontweight='bold')
    ax1.set_title('Złożoność słownictwa: średnia długość słów\n(n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=15, ha='right')
    ax1.set_ylim(5, 7.5)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax1.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    for bar, mean in zip(bars1, means_word):
        ax1.annotate(f'{mean:.2f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Prawy wykres - długość zdań
    means_sent = [np.mean(sent_len_by_version[v]) for v in versions]
    stds_sent = [np.std(sent_len_by_version[v]) for v in versions]
    
    bars2 = ax2.bar(x, means_sent, width, yerr=stds_sent, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Średnia długość zdania (słowa)', fontsize=12, fontweight='bold')
    ax2.set_title('Złożoność składni: średnia długość zdań\n(n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=15, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax2.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    for bar, mean in zip(bars2, means_sent):
        ax2.annotate(f'{mean:.1f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "complexity_comparison")
    
    # ===== WYKRES 2: Scatter plot - korelacja między metrykami =====
    fig2, ax3 = plt.subplots(figsize=(10, 8))
    
    for version in versions:
        ax3.scatter(word_len_by_version[version], sent_len_by_version[version],
                   c=VERSION_COLORS[version], label=VERSION_LABELS[version],
                   s=100, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Dodaj średnie jako większe punkty
    for version in versions:
        mean_word = np.mean(word_len_by_version[version])
        mean_sent = np.mean(sent_len_by_version[version])
        ax3.scatter(mean_word, mean_sent, c=VERSION_COLORS[version],
                   s=300, marker='*', edgecolors='black', linewidth=2, zorder=5)
    
    ax3.set_xlabel('Średnia długość słowa (znaki)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Średnia długość zdania (słowa)', fontsize=12, fontweight='bold')
    ax3.set_title('Korelacja złożoności słownictwa i składni\n(★ = średnia dla wersji, ● = pojedyncze artykuły, n=16)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax3.legend(loc='upper left', bbox_to_anchor=(1.02, 1), title='Wersja tekstu', framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig2, "complexity_correlation")
    
    # ===== WYKRES 3: Violin plot =====
    fig3, (ax4, ax5) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Przygotuj dane do violin plot
    word_data = [word_len_by_version[v] for v in versions]
    sent_data = [sent_len_by_version[v] for v in versions]
    
    # Violin plot dla długości słów
    vp1 = ax4.violinplot(word_data, positions=x, showmeans=True, showmedians=True)
    for i, body in enumerate(vp1['bodies']):
        body.set_facecolor(colors[i])
        body.set_alpha(0.7)
    
    ax4.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Średnia długość słowa (znaki)', fontsize=12, fontweight='bold')
    ax4.set_title('Rozkład długości słów (violin plot)', fontsize=14, fontweight='bold', pad=15)
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels, rotation=15, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax4.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # Violin plot dla długości zdań
    vp2 = ax5.violinplot(sent_data, positions=x, showmeans=True, showmedians=True)
    for i, body in enumerate(vp2['bodies']):
        body.set_facecolor(colors[i])
        body.set_alpha(0.7)
    
    ax5.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Średnia długość zdania (słowa)', fontsize=12, fontweight='bold')
    ax5.set_title('Rozkład długości zdań (violin plot)', fontsize=14, fontweight='bold', pad=15)
    ax5.set_xticks(x)
    ax5.set_xticklabels(labels, rotation=15, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax5.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig3, "complexity_violin")
    plt.close(fig3)
    plt.close(fig1)
    plt.close(fig2)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - ZŁOŻONOŚĆ TEKSTU")
    print("="*60)
    for v in versions:
        print(f"\n{VERSION_LABELS[v]}:")
        stats_word = calculate_stats(word_len_by_version[v])
        stats_sent = calculate_stats(sent_len_by_version[v])
        print(f"  Długość słów: {stats_word['mean']:.2f} ± {stats_word['std']:.2f} znaków")
        print(f"  Długość zdań: {stats_sent['mean']:.1f} ± {stats_sent['std']:.1f} słów")


if __name__ == "__main__":
    create_complexity_charts()

