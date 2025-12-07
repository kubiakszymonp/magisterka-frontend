"""
run_all.py - Uruchamia wszystkie metryki NLP

Użycie:
    python run_all.py

Uruchamia kolejno wszystkie skrypty analityczne i zapisuje wyniki do output/.
"""

import subprocess
import sys
from pathlib import Path

# Lista skryptów do uruchomienia
SCRIPTS = [
    "word_count.py",
    "sentence_count.py",
    "avg_sentence_length.py",
    "readability.py",
    "ttr.py",
    "mtld.py",
    "lexical_density.py",
    "paragraph_count.py",
    "avg_word_length.py",
    "jaccard_similarity.py",
    "tfidf_overlap.py",
]


def main():
    script_dir = Path(__file__).parent
    
    print("=" * 60)
    print("URUCHAMIANIE WSZYSTKICH METRYK NLP")
    print("=" * 60)
    
    failed = []
    
    for script_name in SCRIPTS:
        script_path = script_dir / script_name
        
        print(f"\n{'=' * 60}")
        print(f"▶ {script_name}")
        print("=" * 60)
        
        if not script_path.exists():
            print(f"  POMINIĘTO - plik nie istnieje")
            continue
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(script_dir),
                capture_output=False
            )
            
            if result.returncode != 0:
                failed.append(script_name)
                print(f"  BŁĄD (kod: {result.returncode})")
                
        except Exception as e:
            failed.append(script_name)
            print(f"  BŁĄD: {e}")
    
    print("\n" + "=" * 60)
    print("PODSUMOWANIE")
    print("=" * 60)
    
    if failed:
        print(f"Błędy w {len(failed)} skryptach:")
        for name in failed:
            print(f"  - {name}")
    else:
        print("✓ Wszystkie skrypty wykonane pomyślnie!")
    
    print(f"\nWyniki zapisane w: {script_dir / 'output'}")


if __name__ == "__main__":
    main()

