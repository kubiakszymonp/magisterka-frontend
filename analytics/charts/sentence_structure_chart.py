"""
Wykres: Struktura tekstów (liczba zdań i paragrafów)

OPIS WYKRESU:
Porównuje strukturę tekstów między wersjami poprzez analizę liczby zdań
i paragrafów. Pokazuje jak teksty są segmentowane dla różnych odbiorców.

CO PORÓWNUJE:
- Liczbę zdań w każdej wersji
- Liczbę paragrafów w każdej wersji
- Stosunek zdań do paragrafów (ile zdań na paragraf)

INTERPRETACJA:
- Więcej paragrafów przy podobnej liczbie zdań = krótsze paragrafy = łatwiejszy odbiór
- Teksty dla dzieci mogą mieć więcej podziałów dla lepszej czytelności
- Stosunek zdań/paragraf pokazuje "gęstość" tekstu
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


def create_structure_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    sentence_data = load_aggregated_data("sentence_count")["data"]
    paragraph_data = load_aggregated_data("paragraph_count")["data"]
    
    # Agreguj według wersji
    sentences_by_version = aggregate_by_version(sentence_data)
    paragraphs_by_version = aggregate_by_version(paragraph_data)
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: Porównanie zdań i paragrafów =====
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x = np.arange(len(versions))
    width = 0.6
    labels = [VERSION_LABELS[v] for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    # Lewy wykres - liczba zdań
    means_sent = [np.mean(sentences_by_version[v]) for v in versions]
    stds_sent = [np.std(sentences_by_version[v]) for v in versions]
    
    bars1 = ax1.bar(x, means_sent, width, yerr=stds_sent, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Liczba zdań', fontsize=12, fontweight='bold')
    ax1.set_title('Średnia liczba zdań według wersji\n(n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=15, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax1.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    for bar, mean in zip(bars1, means_sent):
        ax1.annotate(f'{mean:.0f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Prawy wykres - liczba paragrafów
    means_para = [np.mean(paragraphs_by_version[v]) for v in versions]
    stds_para = [np.std(paragraphs_by_version[v]) for v in versions]
    
    bars2 = ax2.bar(x, means_para, width, yerr=stds_para, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Liczba paragrafów', fontsize=12, fontweight='bold')
    ax2.set_title('Średnia liczba paragrafów według wersji\n(n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=15, ha='right')
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax2.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    for bar, mean in zip(bars2, means_para):
        ax2.annotate(f'{mean:.0f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "sentence_paragraph_comparison")
    
    # ===== WYKRES 2: Stosunek zdań do paragrafów =====
    fig2, ax3 = plt.subplots(figsize=(10, 6))
    
    # Oblicz stosunek dla każdego artykułu
    ratios_by_version = {}
    for article in sentence_data.keys():
        for version in sentence_data[article].keys():
            if version not in ratios_by_version:
                ratios_by_version[version] = []
            sent = sentence_data[article][version]
            para = paragraph_data[article].get(version, 1)
            ratios_by_version[version].append(sent / para if para > 0 else sent)
    
    means_ratio = [np.mean(ratios_by_version[v]) for v in versions]
    stds_ratio = [np.std(ratios_by_version[v]) for v in versions]
    
    bars3 = ax3.bar(x, means_ratio, width, yerr=stds_ratio, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax3.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Średnia liczba zdań na paragraf', fontsize=12, fontweight='bold')
    ax3.set_title('Gęstość tekstu: stosunek liczby zdań do paragrafów\n(niższa wartość = krótsze, bardziej przystępne paragrafy, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                       for v in versions]
    ax3.legend(handles=legend_elements, title='Wersja tekstu', loc='upper left', 
               bbox_to_anchor=(1.02, 1), framealpha=0.9, fontsize=10, title_fontsize=11)
    
    for bar, mean in zip(bars3, means_ratio):
        ax3.annotate(f'{mean:.1f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig2, "sentences_per_paragraph")
    plt.close(fig2)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - STRUKTURA TEKSTÓW")
    print("="*60)
    for v in versions:
        print(f"\n{VERSION_LABELS[v]}:")
        stats_sent = calculate_stats(sentences_by_version[v])
        stats_para = calculate_stats(paragraphs_by_version[v])
        stats_ratio = calculate_stats(ratios_by_version[v])
        print(f"  Zdania: {stats_sent['mean']:.1f} ± {stats_sent['std']:.1f}")
        print(f"  Paragrafy: {stats_para['mean']:.1f} ± {stats_para['std']:.1f}")
        print(f"  Zdań/paragraf: {stats_ratio['mean']:.2f} ± {stats_ratio['std']:.2f}")
    
    plt.close(fig1)


if __name__ == "__main__":
    create_structure_charts()

