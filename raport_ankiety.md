# Raport: Struktura ankiet ewaluacyjnych

## 1. Wprowadzenie

W systemie ewaluacji artykułów turystycznych wykorzystywane są dwa typy ankiet:
1. **Ankieta dla pojedynczego artykułu** – służy do oceny pojedynczej wersji artykułu
2. **Ankieta porównawcza** – służy do porównania różnych wersji tego samego artykułu

## 2. Ankieta dla pojedynczego artykułu

### 2.1. Cel ankiety
Ankieta służy do oceny jakości pojedynczej wersji artykułu turystycznego. Pozwala na zebranie opinii użytkownika dotyczących różnych aspektów tekstu.

### 2.2. Pola ankiety

#### 2.2.1. Pola identyfikacyjne (automatycznie wypełniane)
- **placeId** (string) – identyfikator miejsca turystycznego
- **articleStyle** (string) – styl wersji artykułu (np. "adult_full", "adult_short", "child_short")
- **timestamp** (string) – znacznik czasu wypełnienia ankiety

#### 2.2.2. Skale ocen (1-5)
Wszystkie poniższe pola wykorzystują 5-punktową skalę ocen, gdzie:
- 1 = najniższa ocena
- 5 = najwyższa ocena

1. **clarity** (number) – "Zrozumiałość"
   - Ocena stopnia, w jakim tekst jest zrozumiały dla czytelnika

2. **styleMatch** (number) – "Dopasowanie stylu do kategorii"
   - Ocena, czy styl tekstu odpowiada kategorii docelowej (np. dla dorosłych, dla dzieci)

3. **structure** (number) – "Struktura tekstu"
   - Ocena organizacji i struktury tekstu

4. **usefulness** (number) – "Przydatność turystyczna"
   - Ocena praktycznej przydatności informacji zawartych w tekście dla turysty

5. **enjoyment** (number) – "Przyjemność czytania"
   - Ocena subiektywnej przyjemności z czytania tekstu

#### 2.2.3. Ocena długości tekstu
- **length** (enum) – "Długość tekstu"
  - Możliwe wartości:
    - "too_short" – Za krótki
    - "just_right" – W sam raz
    - "too_long" – Za długi

#### 2.2.4. Komentarz
- **comment** (string, opcjonalne) – "Komentarz (opcjonalnie)"
  - Pole tekstowe umożliwiające użytkownikowi dodanie własnych uwag i komentarzy

### 2.3. Podsumowanie pól ankiety dla pojedynczego artykułu

| Pole | Typ | Wymagane | Opis |
|------|-----|----------|------|
| placeId | string | Tak | Identyfikator miejsca |
| articleStyle | string | Tak | Styl wersji artykułu |
| timestamp | string | Tak | Czas wypełnienia |
| clarity | number (1-5) | Tak | Zrozumiałość |
| styleMatch | number (1-5) | Tak | Dopasowanie stylu |
| structure | number (1-5) | Tak | Struktura tekstu |
| usefulness | number (1-5) | Tak | Przydatność turystyczna |
| length | enum | Tak | Długość tekstu |
| enjoyment | number (1-5) | Tak | Przyjemność czytania |
| comment | string | Nie | Komentarz użytkownika |

## 3. Ankieta porównawcza

### 3.1. Cel ankiety
Ankieta porównawcza służy do oceny względnej różnych wersji tego samego artykułu. Użytkownik porównuje trzy wersje:
- **Dorośli – pełny** (adult_full)
- **Dorośli – skrót** (adult_short)
- **Dzieci – skrót** (child_short)

### 3.2. Pola ankiety

#### 3.2.1. Pola identyfikacyjne (automatycznie wypełniane)
- **placeId** (string) – identyfikator miejsca turystycznego
- **timestamp** (string) – znacznik czasu wypełnienia ankiety

#### 3.2.2. Pytania porównawcze
Każde z poniższych pól wymaga wyboru jednej z trzech wersji artykułu:
- "Dorośli – pełny" (adult_full)
- "Dorośli – skrót" (adult_short)
- "Dzieci – skrót" (child_short)

1. **bestOverall** (string) – "Która wersja jest ogólnie najlepsza?"
   - Ogólna ocena porównawcza wszystkich wersji

2. **easiestToUnderstand** (string) – "Najłatwiejsza do zrozumienia?"
   - Ocena, która wersja jest najbardziej zrozumiała

3. **bestForChildren** (string) – "Najlepsza dla dzieci?"
   - Ocena przydatności dla odbiorców dziecięcych

4. **bestForQuickLook** (string) – "Najlepsza do szybkiego podglądu?"
   - Ocena przydatności do szybkiego przeglądu informacji

5. **bestForPlanning** (string) – "Najlepsza do planowania wycieczki?"
   - Ocena przydatności w kontekście planowania podróży

#### 3.2.3. Komentarz
- **comment** (string, opcjonalne) – "Komentarz (opcjonalnie)"
  - Pole tekstowe umożliwiające użytkownikowi dodanie własnych uwag i komentarzy

### 3.3. Podsumowanie pól ankiety porównawczej

| Pole | Typ | Wymagane | Opis |
|------|-----|----------|------|
| placeId | string | Tak | Identyfikator miejsca |
| timestamp | string | Tak | Czas wypełnienia |
| bestOverall | string | Tak | Najlepsza wersja ogólnie |
| easiestToUnderstand | string | Tak | Najłatwiejsza do zrozumienia |
| bestForChildren | string | Tak | Najlepsza dla dzieci |
| bestForQuickLook | string | Tak | Najlepsza do szybkiego podglądu |
| bestForPlanning | string | Tak | Najlepsza do planowania wycieczki |
| comment | string | Nie | Komentarz użytkownika |

## 4. Porównanie ankiet

### 4.1. Różnice w podejściu
- **Ankieta pojedyncza**: Ocena bezwzględna jednej wersji artykułu na skali 1-5
- **Ankieta porównawcza**: Ocena względna, wymagająca wyboru najlepszej wersji w różnych kategoriach

### 4.2. Wspólne elementy
- Oba typy ankiet zawierają opcjonalne pole komentarza
- Oba typy zbierają identyfikatory miejsc i znaczniki czasu
- Oba typy są wypełniane przez użytkowników po przeczytaniu artykułów

### 4.3. Zastosowanie w badaniach
- **Ankieta pojedyncza**: Pozwala na analizę jakości bezwzględnej poszczególnych wersji
- **Ankieta porównawcza**: Pozwala na analizę preferencji użytkowników między wersjami oraz identyfikację najlepszych wersji dla różnych celów

## 5. Metodologia zbierania danych

### 5.1. Implementacja techniczna
- Ankiety są zaimplementowane jako komponenty React (`RatingSingleForm`, `RatingCompareForm`)
- Dane są przesyłane do API (`/api/rate-single`, `/api/rate-compare`)
- Odpowiedzi są przechowywane w formacie JSON

### 5.2. Walidacja danych
- Wszystkie pola wymagane muszą być wypełnione przed wysłaniem
- Skale ocen są ograniczone do wartości 1-5
- Wybory w ankiecie porównawczej są ograniczone do trzech dostępnych wersji

## 6. Wnioski

System ankiet został zaprojektowany tak, aby:
1. Zbierać zarówno oceny bezwzględne (ankieta pojedyncza), jak i względne (ankieta porównawcza)
2. Oceniać różne aspekty jakości tekstu (zrozumiałość, struktura, przydatność, itp.)
3. Uwzględniać różne konteksty użycia (dla dzieci, szybki podgląd, planowanie wycieczki)
4. Pozwalać użytkownikom na dodanie własnych komentarzy

Struktura ankiet umożliwia kompleksową ewaluację jakości generowanych artykułów turystycznych z perspektywy użytkownika końcowego.





