"""
Wykres: Czytelność tekstu (Flesch Reading Ease, Gunning FOG Index)

OPIS WYKRESU:
Porównuje czytelność tekstów używając standardowych wskaźników:
- Flesch Reading Ease: wyższy wynik = łatwiejszy tekst (typowo 0-100)
- Gunning FOG Index: niższy wynik = łatwiejszy tekst (lata edukacji)

Uwaga: Formuły są zoptymalizowane dla j. angielskiego - dla polskiego
wartości mogą być przesunięte, ale wciąż pozwalają na porównania.

CO PORÓWNUJE:
- Czytelność między wersjami tekstów
- Dwie różne miary czytelności

INTERPRETACJA:
- Teksty dla dzieci powinny mieć wyższy Flesch RE i niższy FOG
- Wartości ujemne Flesch RE wskazują na bardzo trudny tekst
- FOG ~17+ = tekst dla absolwentów uczelni wyższych
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


def create_readability_charts():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    
    # Wczytaj dane
    raw_data = load_aggregated_data("readability")["data"]
    
    # Agreguj według wersji dla każdej metryki
    flesch_by_version = aggregate_by_version(raw_data, "flesch_reading_ease")
    fog_by_version = aggregate_by_version(raw_data, "fog_index")
    versions = get_ordered_versions()
    
    # ===== WYKRES 1: Flesch Reading Ease =====
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(versions))
    width = 0.6
    labels = [VERSION_LABELS[v] for v in versions]
    colors = [VERSION_COLORS[v] for v in versions]
    
    means_flesch = [np.mean(flesch_by_version[v]) for v in versions]
    stds_flesch = [np.std(flesch_by_version[v]) for v in versions]
    
    bars1 = ax1.bar(x, means_flesch, width, yerr=stds_flesch, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Granica czytelności')
    ax1.axhline(y=30, color='orange', linestyle='--', alpha=0.5, label='Trudny (30)')
    ax1.axhline(y=60, color='green', linestyle='--', alpha=0.5, label='Standardowy (60)')
    
    ax1.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Flesch Reading Ease', fontsize=12, fontweight='bold')
    ax1.set_title('Wskaźnik czytelności Flesch Reading Ease\n(wyższy = łatwiejszy tekst, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend(loc='upper right', fontsize=9, title='Poziomy czytelności', framealpha=0.9)
    
    # Legenda kolorów wersji
    from matplotlib.patches import Patch
    version_legend = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                      for v in versions]
    ax1.legend(handles=version_legend + ax1.get_legend().get_patches(), 
               title='Wersja tekstu / Poziomy', loc='upper right', framealpha=0.9, fontsize=9)
    
    for bar, mean in zip(bars1, means_flesch):
        y_pos = bar.get_height() + 2 if bar.get_height() >= 0 else bar.get_height() - 8
        ax1.annotate(f'{mean:.1f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5 if bar.get_height() >= 0 else -15), 
                    textcoords='offset points',
                    ha='center', va='bottom' if bar.get_height() >= 0 else 'top',
                    fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig1, "readability_flesch")
    
    # ===== WYKRES 2: Gunning FOG Index =====
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    means_fog = [np.mean(fog_by_version[v]) for v in versions]
    stds_fog = [np.std(fog_by_version[v]) for v in versions]
    
    bars2 = ax2.bar(x, means_fog, width, yerr=stds_fog, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.2,
                   error_kw={'linewidth': 2, 'capthick': 2})
    
    # Linie referencyjne
    ax2.axhline(y=12, color='green', linestyle='--', alpha=0.5, label='Liceum (12)')
    ax2.axhline(y=16, color='orange', linestyle='--', alpha=0.5, label='Studia (16)')
    ax2.axhline(y=20, color='red', linestyle='--', alpha=0.5, label='Bardzo trudny (20)')
    
    ax2.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Gunning FOG Index (lata edukacji)', fontsize=12, fontweight='bold')
    ax2.set_title('Wskaźnik trudności Gunning FOG\n(niższy = łatwiejszy tekst, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend(loc='upper right', fontsize=9, title='Poziomy trudności', framealpha=0.9)
    
    # Legenda kolorów wersji
    from matplotlib.patches import Patch
    version_legend = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', label=VERSION_LABELS[v]) 
                      for v in versions]
    ax2.legend(handles=version_legend + ax2.get_legend().get_patches(), 
               title='Wersja tekstu / Poziomy', loc='upper right', framealpha=0.9, fontsize=9)
    
    for bar, mean in zip(bars2, means_fog):
        ax2.annotate(f'{mean:.1f}',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    save_chart(fig2, "readability_fog")
    
    # ===== WYKRES 3: Porównanie obu wskaźników (dual axis) =====
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    
    x_offset = 0.2
    width = 0.35
    
    # Normalizacja dla porównania (FOG odwrócony, bo niższy = lepszy)
    flesch_norm = [(v - min(means_flesch)) / (max(means_flesch) - min(means_flesch)) * 100 
                   for v in means_flesch]
    fog_norm = [(max(means_fog) - v) / (max(means_fog) - min(means_fog)) * 100 
                for v in means_fog]
    
    bars_flesch = ax3.bar(x - x_offset, flesch_norm, width, label='Flesch RE (normalizowany)',
                          color='#2196F3', edgecolor='black', alpha=0.8)
    bars_fog = ax3.bar(x + x_offset, fog_norm, width, label='FOG (odwrócony, normalizowany)',
                       color='#FF9800', edgecolor='black', alpha=0.8)
    
    ax3.set_xlabel('Wersja tekstu', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Łatwość czytania (0-100, wyższy = łatwiejszy)', fontsize=12, fontweight='bold')
    ax3.set_title('Porównanie wskaźników czytelności (normalizowane)\n(wyższa wartość = łatwiejszy tekst, n=16 artykułów)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels)
    ax3.legend(title='Wskaźnik', framealpha=0.9, fontsize=10, title_fontsize=11)
    ax3.set_ylim(0, 110)
    
    plt.tight_layout()
    save_chart(fig3, "readability_comparison")
    
    # ===== WYKRES 4: Boxplot obu metryk =====
    fig4, (ax4, ax5) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Flesch boxplot
    flesch_data = [flesch_by_version[v] for v in versions]
    bp1 = ax4.boxplot(flesch_data, labels=labels, patch_artist=True,
                      medianprops={'color': 'black', 'linewidth': 2})
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax4.set_ylabel('Flesch Reading Ease', fontsize=12, fontweight='bold')
    ax4.set_title('Rozkład Flesch Reading Ease (boxplot)', fontsize=14, fontweight='bold', pad=15)
    ax4.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax4.legend(handles=legend_elements, title='Wersja tekstu', loc='upper right', 
               framealpha=0.9, fontsize=10, title_fontsize=11)
    
    # FOG boxplot
    fog_data = [fog_by_version[v] for v in versions]
    bp2 = ax5.boxplot(fog_data, labels=labels, patch_artist=True,
                      medianprops={'color': 'black', 'linewidth': 2})
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax5.set_ylabel('Gunning FOG Index', fontsize=12, fontweight='bold')
    ax5.set_title('Rozkład Gunning FOG Index (boxplot)', fontsize=14, fontweight='bold', pad=15)
    
    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=VERSION_COLORS[v], edgecolor='black', alpha=0.7, label=VERSION_LABELS[v]) 
                       for v in versions]
    ax5.legend(handles=legend_elements, title='Wersja tekstu', loc='upper right', 
               framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig4, "readability_boxplot")
    plt.close(fig4)
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - CZYTELNOŚĆ")
    print("="*60)
    for v in versions:
        print(f"\n{VERSION_LABELS[v]}:")
        stats_flesch = calculate_stats(flesch_by_version[v])
        stats_fog = calculate_stats(fog_by_version[v])
        print(f"  Flesch RE: {stats_flesch['mean']:.1f} ± {stats_flesch['std']:.1f}")
        print(f"  FOG Index: {stats_fog['mean']:.1f} ± {stats_fog['std']:.1f}")


if __name__ == "__main__":
    create_readability_charts()

