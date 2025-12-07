"""
Główny skrypt generujący wszystkie wykresy analityczne.

Uruchamia wszystkie skrypty wykresów i eksportuje je do plików obrazów.
"""

import sys
from pathlib import Path

# Dodaj ścieżkę do modułów
sys.path.insert(0, str(Path(__file__).parent))

def run_all_charts():
    """Uruchamia wszystkie skrypty wykresów."""
    
    charts = [
        ("word_count_chart", "Liczba słów"),
        ("sentence_structure_chart", "Struktura tekstów"),
        ("complexity_chart", "Złożoność tekstu"),
        ("readability_chart", "Czytelność"),
        ("ttr_chart", "Bogactwo słownictwa (TTR)"),
        ("mtld_chart", "Różnorodność leksykalna (MTLD)"),
        ("lexical_density_chart", "Gęstość leksykalna"),
        ("jaccard_similarity_chart", "Podobieństwo Jaccarda"),
        ("tfidf_overlap_chart", "TF-IDF Overlap"),
    ]
    
    print("="*70)
    print("GENEROWANIE WYKRESÓW ANALITYCZNYCH")
    print("="*70)
    print()
    
    successful = []
    failed = []
    
    for module_name, description in charts:
        try:
            print(f"📊 Generowanie: {description}...")
            module = __import__(module_name)
            
            # Wywołaj główną funkcję modułu
            if hasattr(module, f"create_{module_name.replace('_chart', '')}_charts"):
                func_name = f"create_{module_name.replace('_chart', '')}_charts"
            elif hasattr(module, "create_charts"):
                func_name = "create_charts"
            else:
                # Spróbuj znaleźć funkcję zaczynającą się od "create_"
                funcs = [name for name in dir(module) if name.startswith("create_")]
                if funcs:
                    func_name = funcs[0]
                else:
                    raise AttributeError(f"Nie znaleziono funkcji create_* w {module_name}")
            
            getattr(module, func_name)()
            successful.append(description)
            print(f"✓ {description} - zakończono pomyślnie\n")
            
        except Exception as e:
            failed.append((description, str(e)))
            print(f"✗ {description} - BŁĄD: {e}\n")
    
    # Podsumowanie
    print("="*70)
    print("PODSUMOWANIE")
    print("="*70)
    print(f"\n✓ Pomyślnie wygenerowano: {len(successful)}/{len(charts)}")
    for desc in successful:
        print(f"  - {desc}")
    
    if failed:
        print(f"\n✗ Niepowodzenia: {len(failed)}/{len(charts)}")
        for desc, error in failed:
            print(f"  - {desc}: {error}")
    
    print("\n" + "="*70)
    print(f"Wykresy zapisane w: {Path(__file__).parent / 'output'}")
    print("="*70)


if __name__ == "__main__":
    run_all_charts()

