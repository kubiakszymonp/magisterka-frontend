# Raport Metryk Analizy Tekstów NLP

## Wprowadzenie

Niniejszy raport opisuje kompleksowy system metryk zastosowany do analizy tekstów generowanych przez system adaptacji treści. System analizuje trzy wersje każdego artykułu:
- **adult_full**: Wersja pełna dla dorosłych
- **adult_short**: Wersja skrócona dla dorosłych
- **child_short**: Wersja skrócona dla dzieci

Wszystkie metryki zostały obliczone dla 16 artykułów, a wyniki zostały zwizualizowane w postaci wykresów statystycznych.

---

## 1. Metryki Ilościowe

### 1.1. Liczba słów (Word Count)

**Opis metryki:**
Liczba słów to podstawowa metryka ilościowa tekstu. Zlicza wszystkie tokeny alfabetyczne w tekście, pomijając cyfry, interpunkcję i symbole. Tokenizacja odbywa się przy użyciu biblioteki spaCy z modelem języka polskiego.

**Wzór:**
```
Word Count = liczba tokenów alfabetycznych
```

**Znaczenie dla projektu:**
- Pozwala porównać objętość różnych wersji artykułów (full vs short)
- Weryfikuje, czy generator przestrzega limitów długości tekstu
- Stanowi bazę do obliczania innych wskaźników (np. średnia długość zdania)
- Wersja pełna powinna mieć znacząco więcej słów niż wersje skrócone

**Interpretacja wyników:**
- Wyższa wartość = dłuższy tekst
- Duży rozrzut wartości może wskazywać na niejednolitość generowania
- Porównanie między wersjami pokazuje efektywność procesu skracania tekstu

**Wykresy:**
1. **word_count_bar.png** - Wykres słupkowy ze średnimi wartościami i odchyleniami standardowymi dla każdej wersji. Pokazuje średnią liczbę słów z przedziałami ufności.
2. **word_count_boxplot.png** - Wykres pudełkowy (boxplot) pokazujący rozkład liczby słów. Prezentuje medianę, kwartyle (Q1-Q3), zakres oraz wartości odstające. Punkty reprezentują pojedyncze artykuły.

---

### 1.2. Liczba zdań (Sentence Count)

**Opis metryki:**
Liczba zdań zlicza wszystkie zdania w tekście. Wykorzystuje tokenizator zdań z biblioteki spaCy, który rozpoznaje końcówki zdań (kropki, pytajniki, wykrzykniki) oraz kontekst, co pozwala na prawidłowe rozdzielenie zdań nawet w przypadku skrótów.

**Wzór:**
```
Sentence Count = liczba zdań w tekście
```

**Znaczenie dla projektu:**
- Analiza struktury tekstu i jego segmentacji
- Obliczanie średniej długości zdania (w połączeniu z liczbą słów)
- Porównanie złożoności składniowej między wersjami
- Teksty dla dzieci powinny mieć więcej krótszych zdań dla lepszej czytelności

**Interpretacja wyników:**
- Wyższa wartość = więcej zdań w tekście
- W połączeniu z liczbą słów pozwala ocenić średnią długość zdania
- Więcej zdań przy podobnej liczbie słów = prostszy, bardziej przystępny tekst

**Wykresy:**
1. **sentence_count.png** - Wykres słupkowy pokazujący średnią liczbę zdań dla każdej wersji tekstu z odchyleniami standardowymi.

---

### 1.3. Liczba paragrafów (Paragraph Count)

**Opis metryki:**
Zlicza liczbę akapitów w tekście. Akapit definiowany jest jako blok tekstu oddzielony pustymi liniami (podwójnymi znakami nowej linii).

**Wzór:**
```
Paragraph Count = liczba bloków tekstu oddzielonych pustymi liniami
```

**Znaczenie dla projektu:**
- Ocena struktury i organizacji tekstu
- Porównanie organizacji treści między wersjami
- Więcej paragrafów przy podobnej liczbie zdań = krótsze paragrafy = łatwiejszy odbiór
- Teksty dla dzieci mogą mieć więcej podziałów dla lepszej czytelności wizualnej

**Interpretacja wyników:**
- Więcej akapitów = lepiej podzielony tekst, bardziej przystępny wizualnie
- Mniej akapitów = bardziej zwarty tekst
- Stosunek zdań do paragrafów pokazuje "gęstość" tekstu

**Wykresy:**
1. **paragraph_count.png** - Wykres słupkowy ze średnią liczbą paragrafów dla każdej wersji.
2. **sentences_per_paragraph.png** - Wykres pokazujący stosunek liczby zdań do paragrafów. Niższa wartość oznacza krótsze, bardziej przystępne paragrafy.

---

## 2. Metryki Złożoności

### 2.1. Średnia długość słowa (Average Word Length)

**Opis metryki:**
Średnia długość słowa mierzy przeciętną liczbę znaków w słowach tekstu. Jest wskaźnikiem złożoności słownictwa.

**Wzór:**
```
AWL = suma długości wszystkich słów / liczba słów
```

**Znaczenie dla projektu:**
- Ocena złożoności słownictwa używanego w tekstach
- Porównanie między wersjami (adult vs child) - teksty dla dzieci powinny mieć niższą wartość
- Uzupełnienie metryki rzadkich słów i gęstości leksykalnej
- Dłuższe słowa często wskazują na bardziej specjalistyczne lub złożone słownictwo

**Interpretacja wyników:**
- Wyższa wartość = dłuższe, bardziej złożone słowa
- Niższa wartość = krótsze, prostsze słowa
- Typowe wartości dla języka polskiego: 5-7 znaków
- Teksty dla dzieci powinny mieć niższą wartość (prostsze słownictwo)

**Wykresy:**
1. **complexity_word_length.png** - Wykres słupkowy ze średnią długością słów dla każdej wersji.
2. **complexity_word_length_violin.png** - Wykres violin plot pokazujący pełny rozkład długości słów z gęstością prawdopodobieństwa.

---

### 2.2. Średnia długość zdania (Average Sentence Length)

**Opis metryki:**
Średnia długość zdania to stosunek liczby słów do liczby zdań w tekście. Jest kluczowym wskaźnikiem złożoności składniowej.

**Wzór:**
```
ASL = liczba słów / liczba zdań
```

**Znaczenie dla projektu:**
- Ocena czytelności tekstu i złożoności składniowej
- Porównanie między wersjami (adult vs child) - teksty dla dzieci powinny mieć niższą ASL
- Analiza stylu pisania generatora
- Krótsze zdania są łatwiejsze w odbiorze i zrozumieniu

**Interpretacja wyników:**
- Niższa wartość (10-15 słów) = prostszy tekst, łatwiejszy w odbiorze
- Wyższa wartość (20+ słów) = bardziej złożony tekst, trudniejszy w odbiorze
- Teksty dla dzieci powinny mieć niższą ASL
- Teksty naukowe/formalne mają wyższą ASL

**Wykresy:**
1. **complexity_sentence_length.png** - Wykres słupkowy ze średnią długością zdań dla każdej wersji.
2. **complexity_sentence_length_violin.png** - Wykres violin plot pokazujący rozkład długości zdań.
3. **complexity_correlation.png** - Wykres rozrzutu (scatter plot) pokazujący korelację między średnią długością słów a średnią długością zdań. Gwiazdki reprezentują średnie dla każdej wersji, kropki - pojedyncze artykuły.

---

## 3. Metryki Różnorodności Leksykalnej

### 3.1. Type-Token Ratio (TTR)

**Opis metryki:**
Type-Token Ratio (TTR) mierzy różnorodność leksykalną tekstu. Jest to stosunek unikalnych słów (types) do wszystkich słów (tokens). Analizujemy dwie wersje:
- **ttr_tokens**: na podstawie form słów (jak w tekście)
- **ttr_lemmas**: na podstawie lemmatów (form podstawowych) - bardziej sprawiedliwy dla polskiego ze względu na bogatą odmianę

**Wzór:**
```
TTR = liczba unikalnych słów / liczba wszystkich słów
```

**Znaczenie dla projektu:**
- Ocena bogactwa słownictwa generowanych tekstów
- Porównanie różnorodności leksykalnej między wersjami
- TTR na lemmatach jest bardziej sprawiedliwy dla języka polskiego (różne formy → ten sam lemat)

**Interpretacja wyników:**
- Wartość od 0 do 1 (często wyrażana jako procent 0-100%)
- Wyższa wartość = większa różnorodność słownictwa
- Niższa wartość = więcej powtórzeń, bardziej ograniczone słownictwo
- Typowe wartości: 0.4-0.6 (40-60%)
- **Ograniczenie**: TTR jest wrażliwy na długość tekstu - dłuższe teksty mają niższy TTR (bo słowa się powtarzają). Dlatego porównywanie TTR między tekstami o różnej długości jest problematyczne.

**Wykresy:**
1. **ttr_tokens.png** - Wykres słupkowy pokazujący TTR obliczony na tokenach dla każdej wersji.
2. **ttr_lemmas.png** - Wykres słupkowy pokazujący TTR obliczony na lemmatach dla każdej wersji.
3. **ttr_correlation.png** - Wykres rozrzutu pokazujący korelację między TTR tokenów a TTR lemmatów. Punkty poniżej linii y=x oznaczają, że lematyzacja redukuje liczbę unikalnych form.

---

### 3.2. Measure of Textual Lexical Diversity (MTLD)

**Opis metryki:**
MTLD to zaawansowana miara różnorodności leksykalnej, która jest odporna na długość tekstu (w przeciwieństwie do TTR). Analizujemy dwie wersje:
- **mtld_tokens**: na podstawie form słów
- **mtld_lemmas**: na podstawie lemmatów

**Algorytm:**
1. Przechodzi przez tekst słowo po słowie
2. Oblicza TTR dla narastającego fragmentu
3. Gdy TTR spada poniżej progu (domyślnie 0.72), kończy "faktor"
4. Zlicza liczbę faktorów i oblicza średnią ich długość
5. Powtarza proces od końca tekstu (bi-directional)
6. Końcowy MTLD to średnia z obu kierunków

**Znaczenie dla projektu:**
- Ocena bogactwa słownictwa generowanych tekstów
- Porównanie różnorodności między wersjami artykułów (można porównywać teksty o różnej długości)
- Analiza czy teksty dla dzieci mają prostsze słownictwo
- **Zaleta nad TTR**: Nie zależy od długości tekstu, można porównywać teksty o różnej długości, bardziej stabilna miara

**Interpretacja wyników:**
- Wyższa wartość = większa różnorodność leksykalna
- Typowe wartości: 50-150
- < 50: niskie zróżnicowanie słownictwa
- 50-100: umiarkowane zróżnicowanie
- > 100: wysokie zróżnicowanie słownictwa
- > 200: dobra różnorodność

**Wykresy:**
1. **mtld_tokens.png** - Wykres słupkowy pokazujący MTLD obliczony na tokenach. Linie referencyjne pokazują poziomy: 100 (akceptowalne) i 200 (dobre).
2. **mtld_lemmas.png** - Wykres słupkowy pokazujący MTLD obliczony na lemmatach.
3. **mtld_tokens_boxplot.png** - Wykres pudełkowy pokazujący rozkład MTLD dla tokenów.
4. **mtld_lemmas_boxplot.png** - Wykres pudełkowy pokazujący rozkład MTLD dla lemmatów.
5. **mtld_vs_length.png** - Wykres rozrzutu pokazujący związek między MTLD a długością tekstu (liczba słów). MTLD powinno być stabilne niezależnie od długości.
6. **mtld_violin.png** - Wykres violin plot porównujący rozkład MTLD dla tokenów i lemmatów.

---

## 4. Metryki Gęstości Informacyjnej

### 4.1. Gęstość leksykalna (Lexical Density)

**Opis metryki:**
Gęstość leksykalna mierzy proporcję słów treściowych (content words) do wszystkich słów w tekście, wyrażaną w procentach.

**Słowa treściowe (content words):**
- Rzeczowniki (NOUN)
- Czasowniki (VERB)
- Przymiotniki (ADJ)
- Przysłówki (ADV)

**Słowa funkcyjne (function words):**
- Przyimki, spójniki, zaimki, rodzajniki, partykuły, etc.
- Pełnią rolę gramatyczną, nie niosą głównego znaczenia

**Wzór:**
```
Lexical Density = (liczba słów treściowych / liczba wszystkich słów) × 100%
```

**Znaczenie dla projektu:**
- Ocena "gęstości informacyjnej" tekstu
- Porównanie stylu między wersjami (adult vs child)
- Teksty dla dzieci mogą mieć niższą gęstość (więcej słów funkcyjnych dla lepszego zrozumienia)
- Teksty naukowe/specjalistyczne mają wyższą gęstość

**Interpretacja wyników:**
- Wyższa wartość (50-70%) = tekst gęsty informacyjnie, trudniejszy
- Niższa wartość (40-50%) = tekst bardziej konwersacyjny/potoczny, łatwiejszy
- Typowe wartości:
  - Teksty pisane: 40-65%
  - Teksty mówione: 35-50%
  - Teksty naukowe: 55-70%

**Wykresy:**
1. **lexical_density_bar.png** - Wykres słupkowy ze średnią gęstością leksykalną. Linie referencyjne pokazują poziomy: 50% (typowy) i 60% (wysoka gęstość).
2. **lexical_density_boxplot.png** - Wykres pudełkowy pokazujący rozkład gęstości leksykalnej.
3. **lexical_density_histogram.png** - Trzy histogramy (jeden dla każdej wersji) pokazujące dystrybucję gęstości leksykalnej.
4. **lexical_density_vs_word_length.png** - Wykres rozrzutu pokazujący korelację między gęstością leksykalną a średnią długością słów. Dłuższe słowa często oznaczają więcej słów znaczących.

---

## 5. Metryki Czytelności

### 5.1. Flesch Reading Ease (FRE)

**Opis metryki:**
Flesch Reading Ease mierzy łatwość czytania tekstu na skali 0-100. Wzór został stworzony dla języka angielskiego, ale został zaadaptowany dla polskiego.

**Wzór (adaptowany dla polskiego):**
```
FRE = 206.835 - (1.015 × ASL) - (84.6 × ASW)
```
gdzie:
- ASL = średnia długość zdania (w słowach)
- ASW = średnia liczba sylab na słowo

**Znaczenie dla projektu:**
- Ocena dostosowania tekstu do grupy docelowej (adult vs child)
- Porównanie czytelności różnych wersji artykułów
- Teksty dla dzieci powinny mieć wyższy wynik FRE

**Interpretacja wyników:**
- 90-100: Bardzo łatwy (dla 11-latków)
- 80-89: Łatwy
- 70-79: Dość łatwy
- 60-69: Standardowy
- 50-59: Dość trudny
- 30-49: Trudny
- 0-29: Bardzo trudny (akademicki)
- Wartości ujemne wskazują na bardzo trudny tekst

**Uwaga:** Wzory zostały stworzone dla języka angielskiego. Dla polskiego wyniki mogą być przesunięte ze względu na różnice w morfologii (polski ma więcej sylab na słowo). Wartości są porównywalne między tekstami polskimi, ale nie bezpośrednio z angielskimi benchmarkami.

**Wykresy:**
1. **readability_flesch.png** - Wykres słupkowy pokazujący średni wynik Flesch Reading Ease dla każdej wersji. Linie referencyjne pokazują poziomy: 0 (granica czytelności), 30 (trudny), 60 (standardowy).
2. **readability_flesch_boxplot.png** - Wykres pudełkowy pokazujący rozkład wyników FRE.

---

### 5.2. Gunning Fog Index (FOG)

**Opis metryki:**
Gunning Fog Index szacuje liczbę lat edukacji potrzebnych do zrozumienia tekstu. Niższy wynik oznacza łatwiejszy tekst.

**Wzór:**
```
FOG = 0.4 × (ASL + PHW)
```
gdzie:
- ASL = średnia długość zdania
- PHW = procent "trudnych słów" (3+ sylaby)

**Znaczenie dla projektu:**
- Ocena trudności tekstu w kategoriach edukacyjnych
- Porównanie między wersjami - teksty dla dzieci powinny mieć niższy FOG
- Uzupełnienie metryki Flesch Reading Ease

**Interpretacja wyników:**
- 6: Bardzo łatwy (szkoła podstawowa)
- 8-10: Łatwy (gimnazjum)
- 10-12: Średni (liceum)
- 12-14: Trudny (studia)
- 14+: Bardzo trudny (specjalistyczny)
- ~17+: Tekst dla absolwentów uczelni wyższych

**Wykresy:**
1. **readability_fog.png** - Wykres słupkowy pokazujący średni wynik Gunning Fog Index. Linie referencyjne pokazują poziomy: 12 (liceum), 16 (studia), 20 (bardzo trudny).
2. **readability_fog_boxplot.png** - Wykres pudełkowy pokazujący rozkład wyników FOG.
3. **readability_comparison.png** - Wykres porównujący oba wskaźniki czytelności (FRE i FOG) w formie znormalizowanej. Wyższa wartość oznacza łatwiejszy tekst.

---

## 6. Metryki Podobieństwa

### 6.1. Indeks Jaccarda (Jaccard Similarity)

**Opis metryki:**
Indeks Jaccarda mierzy podobieństwo między dwoma zbiorami słów. Oblicza stosunek części wspólnej do sumy zbiorów. W projekcie porównujemy pary wersji artykułów na podstawie zbiorów lemmatów (form podstawowych).

**Wzór:**
```
J(A, B) = |A ∩ B| / |A ∪ B|
```
gdzie A i B to zbiory unikalnych lemmatów z dwóch wersji tekstu.

**Porównywane pary:**
- adult_full ↔ adult_short
- adult_full ↔ child_short
- adult_short ↔ child_short

**Znaczenie dla projektu:**
- Ocena jak bardzo różnią się wersje artykułu pod względem użytego słownictwa
- Sprawdzenie czy wersja dla dzieci używa podobnego słownictwa co dorosła
- Wersje dla tego samego odbiorcy powinny być bardziej podobne
- Niskie podobieństwo może wskazywać na różne podejście do tematu

**Interpretacja wyników:**
- Wartość od 0 do 1
- 0 = brak wspólnych słów
- 1 = identyczne zbiory słów
- Typowe wartości między wersjami: 0.3-0.7
- Wyższe podobieństwo = więcej wspólnego słownictwa

**Wykresy:**
1. **jaccard_bar.png** - Wykres słupkowy pokazujący średni indeks Jaccarda dla każdej pary wersji.
2. **jaccard_boxplot.png** - Wykres pudełkowy pokazujący rozkład podobieństwa Jaccarda. Punkty reprezentują pojedyncze artykuły.
3. **jaccard_heatmap.png** - Macierz podobieństwa (heatmapa) pokazująca średnie wartości Jaccarda między wszystkimi parami wersji. Kolor intensywniejszy = większe podobieństwo.
4. **jaccard_violin.png** - Wykres violin plot pokazujący pełny rozkład podobieństwa dla każdej pary wersji.

---

### 6.2. TF-IDF Overlap

**Opis metryki:**
TF-IDF Overlap mierzy podobieństwo między wersjami artykułu na podstawie najważniejszych słów kluczowych wyodrębnionych metodą TF-IDF (Term Frequency-Inverse Document Frequency).

**Metoda:**
1. Dla każdej wersji oblicz TF-IDF
2. Wyodrębnij top N słów kluczowych (najwyższe TF-IDF, w projekcie N=20)
3. Oblicz overlap między zbiorami keywords różnych wersji

**TF-IDF:**
- TF (Term Frequency) = częstość słowa w dokumencie
- IDF (Inverse Document Frequency) = log(liczba dokumentów / dokumenty zawierające słowo)
- TF-IDF = TF × IDF (wyższa wartość = słowo jest ważniejsze w kontekście dokumentu)

**Wartości wyrażone w procentach (0-100%):**
- 100% = wszystkie kluczowe terminy są wspólne
- 0% = brak wspólnych kluczowych terminów

**Porównywane pary:**
- adult_full ↔ adult_short
- adult_full ↔ child_short
- adult_short ↔ child_short

**Znaczenie dla projektu:**
- Sprawdzenie czy różne wersje zachowują te same kluczowe pojęcia
- Analiza czy uproszczenie tekstu (child) nie traci ważnych słów kluczowych
- Wysoki overlap = wersje skupiają się na tych samych aspektach tematu
- Niski overlap = różne wersje podkreślają różne aspekty

**Interpretacja wyników:**
- Wyższa wartość = więcej wspólnych słów kluczowych
- Pokazuje czy wersje zachowują te same główne tematy/koncepty
- Oczekujemy wyższego overlap dla wersji dla tego samego odbiorcy

**Wykresy:**
1. **tfidf_bar.png** - Wykres słupkowy pokazujący średni TF-IDF Overlap dla każdej pary wersji. Linie referencyjne pokazują poziomy: 50% i 70% (wysoki overlap).
2. **tfidf_boxplot.png** - Wykres pudełkowy pokazujący rozkład TF-IDF Overlap.
3. **tfidf_heatmap.png** - Macierz overlap (heatmapa) pokazująca średnie wartości TF-IDF Overlap między wszystkimi parami wersji.
4. **tfidf_vs_jaccard.png** - Wykres porównujący TF-IDF Overlap z indeksem Jaccarda (przeskalowanym ×100 dla porównania). Pokazuje różnice między podobieństwem ogólnym (Jaccard) a podobieństwem kluczowych terminów (TF-IDF).
5. **tfidf_jaccard_correlation.png** - Wykres rozrzutu pokazujący korelację między TF-IDF Overlap a indeksem Jaccarda dla każdej pary wersji.

---

## Podsumowanie Metryk

### Metryki Ilościowe
- **Liczba słów**: Podstawowa metryka objętości tekstu
- **Liczba zdań**: Analiza struktury i segmentacji
- **Liczba paragrafów**: Ocena organizacji tekstu

### Metryki Złożoności
- **Średnia długość słowa**: Złożoność słownictwa
- **Średnia długość zdania**: Złożoność składniowa

### Metryki Różnorodności Leksykalnej
- **TTR (Type-Token Ratio)**: Różnorodność słownictwa (wrażliwa na długość)
- **MTLD**: Różnorodność leksykalna (odporna na długość)

### Metryki Gęstości Informacyjnej
- **Gęstość leksykalna**: Proporcja słów znaczących

### Metryki Czytelności
- **Flesch Reading Ease**: Łatwość czytania (0-100)
- **Gunning Fog Index**: Trudność tekstu (lata edukacji)

### Metryki Podobieństwa
- **Indeks Jaccarda**: Podobieństwo słownictwa między wersjami
- **TF-IDF Overlap**: Podobieństwo kluczowych terminów między wersjami

---

## Wnioski i Zastosowanie

System metryk pozwala na kompleksową ocenę:
1. **Ilościową**: Objętość i struktura tekstów
2. **Jakościową**: Złożoność, różnorodność, czytelność
3. **Porównawczą**: Podobieństwo między wersjami dla różnych grup odbiorców

Wszystkie metryki zostały obliczone dla 16 artykułów w trzech wersjach, co pozwala na:
- Statystyczną analizę różnic między wersjami
- Weryfikację czy generator poprawnie dostosowuje teksty do grup docelowych
- Identyfikację obszarów wymagających poprawy w procesie generowania

Wykresy wizualizują wyniki w sposób umożliwiający szybką interpretację i porównanie wartości między wersjami tekstów.

