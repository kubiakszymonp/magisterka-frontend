"""
Uruchamia wszystkie skrypty generujące wykresy dla analizy ratingów.

Wykresy Single (oceny pojedynczych artykułów) - 4 wykresy:
1. single_avg_ratings_by_style.png - Średnie ocen wg typu artykułu (#1)
2. single_heatmap_age_style.png - Heatmapa wiek × styl (#4)
3. single_violin_ratings.png - Violin plot rozkładu ocen (S-A)
4. single_length_perception_stacked.png - Postrzeganie długości (S-D)

Wykresy Compare (porównania między wersjami) - 5 wykresów:
5. compare_wins_by_category.png - Zwycięstwa wg kategorii (#7)
6. compare_best_overall_pie.png - Najlepsza wersja ogólnie (#8)
7. compare_preferences_by_age_stacked.png - Preferencje wg wieku (#9)
8. compare_domination.png - Analiza dominacji (C-B)
9. compare_consensus.png - Konsensus per kategoria (C-C)

Wszystkie wykresy zapisywane są w folderze output/ jako PNG.
"""

import sys
from pathlib import Path

# Dodaj ścieżkę do modułów
sys.path.insert(0, str(Path(__file__).parent))

def run_all_charts():
    print("=" * 70)
    print("GENEROWANIE WYKRESÓW - ANALIZA RATINGÓW Z ANKIET")
    print("=" * 70)
    
    # ===== SINGLE RATINGS =====
    print("\n" + "=" * 70)
    print("WYKRESY DLA SINGLE RATINGS (oceny pojedynczych artykułów)")
    print("=" * 70)
    
    print("\n>>> 1/4: Średnie ocen według typu artykułu (#1)")
    try:
        from single_avg_ratings import create_avg_ratings_chart
        create_avg_ratings_chart()
        print("✓ Zakończono: single_avg_ratings_by_style.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 2/4: Heatmapa wiek × styl (#4)")
    try:
        from single_heatmap_age_style import create_heatmap_age_style
        create_heatmap_age_style()
        print("✓ Zakończono: single_heatmap_age_style.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 3/4: Violin plot rozkładu ocen (S-A)")
    try:
        from single_violin_ratings import create_violin_ratings_chart
        create_violin_ratings_chart()
        print("✓ Zakończono: single_violin_ratings.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 4/4: Postrzeganie długości artykułów (S-D)")
    try:
        from single_length_perception import create_length_perception_chart
        create_length_perception_chart()
        print("✓ Zakończono: single_length_perception_stacked.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    # ===== COMPARE RATINGS =====
    print("\n" + "=" * 70)
    print("WYKRESY DLA COMPARE RATINGS (porównania między wersjami)")
    print("=" * 70)
    
    print("\n>>> 1/5: Zwycięstwa według kategorii (#7)")
    try:
        from compare_wins_by_category import create_wins_by_category_chart
        create_wins_by_category_chart()
        print("✓ Zakończono: compare_wins_by_category.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 2/5: Najlepsza wersja ogólnie - pie chart (#8)")
    try:
        from compare_best_overall_pie import create_best_overall_pie_chart
        create_best_overall_pie_chart()
        print("✓ Zakończono: compare_best_overall_pie.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 3/5: Preferencje według grupy wiekowej (#9)")
    try:
        from compare_preferences_by_age import create_preferences_by_age_chart
        create_preferences_by_age_chart()
        print("✓ Zakończono: compare_preferences_by_age_stacked.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 4/5: Analiza dominacji (C-B)")
    try:
        from compare_domination import create_domination_chart
        create_domination_chart()
        print("✓ Zakończono: compare_domination.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    print("\n>>> 5/5: Konsensus per kategoria (C-C)")
    try:
        from compare_consensus import create_consensus_chart
        create_consensus_chart()
        print("✓ Zakończono: compare_consensus.png\n")
    except Exception as e:
        print(f"✗ Błąd: {e}\n")
    
    # Podsumowanie
    print("\n" + "=" * 70)
    print("PODSUMOWANIE")
    print("=" * 70)
    
    output_dir = Path(__file__).parent / "output"
    if output_dir.exists():
        png_files = list(output_dir.glob("*.png"))
        print(f"\n✓ Wygenerowano {len(png_files)} wykresów w folderze:")
        print(f"  {output_dir}")
        print("\nLista plików:")
        for f in sorted(png_files):
            print(f"  - {f.name}")
    else:
        print("\n✗ Folder output nie istnieje")


if __name__ == "__main__":
    run_all_charts()

