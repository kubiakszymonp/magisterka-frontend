"""
Wykres: Liczba słów (Word Count)

OPIS WYKRESU:
Porównuje objętość tekstów między trzema wersjami: dziecięcą (krótką), 
dorosłą (krótką) i dorosłą (pełną). Pokazuje jak różnią się długości 
tekstów generowanych dla różnych grup odbiorców.

CO PORÓWNUJE:
- Średnią liczbę słów w każdej wersji
- Rozrzut wartości (odchylenie standardowe)
- Rozkład długości tekstów (boxplot)

INTERPRETACJA:
- Wersja pełna powinna mieć znacząco więcej słów
- Wersje krótkie powinny być porównywalne długością
- Duży rozrzut może wskazywać na niejednolitość generowania
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


def create_word_count_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("word_count")
    data = raw_data["data"]
    
    # Agreguj według wersji
    by_version = aggregate_by_version(data)
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: Wykres słupkowy ze średnimi =====
    fig1, ax1 = plt.subplots(figsize=(10, 7))
    
    x = np.arange(len(versions))
    width = 0.6
    
    means = [np.mean(by_version[v]) for v in versions]
    stds = [np.std(by_version[v]) for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    labels = [VERSION_LABELS[v] for v in versions]
    
    bars = ax1.bar(x, means, width, yerr=stds, capsize=5, 
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Liczba słów', fontsize=12, fontweight='bold')
    ax1.set_title('Objętość tekstów wg wersji\n(średnia ± odchylenie standardowe, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_ylim(0, max(means) * 1.3)
    
    # Dodaj wartości na słupkach
    for bar, mean, std in zip(bars, means, stds):
        ax1.annotate(f'{mean:.0f}±{std:.0f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 8), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Legenda kolorów
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax1.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig1, "word_count_bar")
    plt.close(fig1)
    
    # ===== WYKRES 2: Boxplot =====
    fig2, ax2 = plt.subplots(figsize=(10, 7))
    
    # Przygotuj dane do boxplot
    plot_data = [by_version[v] for v in versions]
    
    bp = ax2.boxplot(plot_data, labels=labels, patch_artist=True,
                     medianprops={'color': 'black', 'linewidth': 2},
                     whiskerprops={'linewidth': 1.5},
                     capprops={'linewidth': 1.5})
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Liczba słów', fontsize=12, fontweight='bold')
    ax2.set_title('Rozkład liczby słów wg wersji tekstu\n(mediana, kwartyle Q1-Q3, zakres)', 
                  fontsize=14, fontweight='bold', pad=15)
    
    # Dodaj punkty dla każdego artykułu
    for i, (version, vals) in enumerate(zip(versions, plot_data)):
        jitter = np.random.normal(0, 0.04, len(vals))
        ax2.scatter(np.ones(len(vals)) * (i + 1) + jitter, vals, 
                   alpha=0.6, s=40, c='black', zorder=3, label='Pojedyncze artykuły' if i == 0 else '')
    
    # Legenda
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
                                  markersize=8, alpha=0.6, label='Pojedyncze artykuły'))
    ax2.legend(handles=legend_elements, title='Legenda', loc='upper left', 
               framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig2, "word_count_boxplot")
    plt.close(fig2)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - LICZBA SŁÓW")
    print("="*60)
    for v in versions:
        stats = calculate_stats(by_version[v])
        print(f"\n{VERSION_LABELS[v]}:")
        print(f"  Średnia: {stats['mean']:.1f} ± {stats['std']:.1f}")
        print(f"  Mediana: {stats['median']:.1f}")
        print(f"  Zakres: {stats['min']:.0f} - {stats['max']:.0f}")


if __name__ == "__main__":
    create_word_count_charts()
