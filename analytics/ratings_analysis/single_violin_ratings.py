"""
Wykres S-A: Violin/Box plot rozkładu ocen

OPIS WYKRESU:
Violin plot lub box plot pokazujący pełny rozkład ocen dla każdego 
typu artykułu w każdej kategorii oceny.

CO PORÓWNUJE:
- Rozkład ocen (nie tylko średnią)
- Medianę, kwartyle, rozrzut wartości

INTERPRETACJA:
- Szersze "skrzypce" = większy rozrzut ocen
- Pozwala zobaczyć czy oceny są spójne czy polaryzujące
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    load_single_ratings, aggregate_single_by_style, calculate_stats,
    setup_polish_matplotlib, save_chart, get_ordered_versions,
    VERSION_LABELS, VERSION_COLORS, RATING_FIELDS, RATING_LABELS
)
import numpy as np


def create_violin_ratings_chart():
    plt = setup_polish_matplotlib()
    import seaborn as sns
    from matplotlib.patches import Patch
    
    # Wczytaj dane
    data = load_single_ratings()
    versions = get_ordered_versions()
    
    print(f"Wczytano {len(data)} ocen z ankiety single")
    
    # Przygotuj dane w formacie długim dla seaborn
    plot_data = []
    for entry in data:
        style = entry.get("articleStyle")
        if style in versions:
            for field in RATING_FIELDS:
                value = entry.get(field)
                if value is not None:
                    plot_data.append({
                        "Typ artykułu": VERSION_LABELS[style],
                        "Kategoria": RATING_LABELS[field],
                        "Ocena": value,
                        "style_key": style
                    })
    
    import pandas as pd
    df = pd.DataFrame(plot_data)
    
    # ===== WYKRES 1: Violin plot dla każdej kategorii =====
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Kolejność kategorii i typów
    category_order = [RATING_LABELS[f] for f in RATING_FIELDS]
    hue_order = [VERSION_LABELS[v] for v in versions]
    palette = {VERSION_LABELS[v]: VERSION_COLORS[v] for v in versions}
    
    sns.violinplot(data=df, x="Kategoria", y="Ocena", hue="Typ artykułu",
                   order=category_order, hue_order=hue_order, palette=palette,
                   ax=ax, inner="box", cut=0)
    
    ax.set_xlabel('Kategoria oceny', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ocena (1-5)', fontsize=12, fontweight='bold')
    ax.set_title(f'Rozkład ocen według typu artykułu (violin plot)\n(n={len(data)} ocen)', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha='right')
    
    # Legenda po prawej stronie
    ax.legend(title='Typ artykułu', loc='upper left', bbox_to_anchor=(1.02, 1), 
              framealpha=0.9, fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    save_chart(fig, "single_violin_ratings")
    plt.close(fig)
    
    # Wyświetl statystyki
    print("\n" + "="*60)
    print("STATYSTYKI - ROZKŁAD OCEN")
    print("="*60)
    
    for version in versions:
        print(f"\n{VERSION_LABELS[version]}:")
        all_ratings = []
        for field in RATING_FIELDS:
            by_style = aggregate_single_by_style(data, field)
            all_ratings.extend(by_style[version])
        
        stats = calculate_stats(all_ratings)
        print(f"  Średnia: {stats['mean']:.2f} ± {stats['std']:.2f}")
        print(f"  Mediana: {stats['median']:.1f}")
        print(f"  Zakres: {stats['min']:.0f} - {stats['max']:.0f}")
        print(f"  Q1-Q3: {stats['q25']:.1f} - {stats['q75']:.1f}")


if __name__ == "__main__":
    create_violin_ratings_chart()

