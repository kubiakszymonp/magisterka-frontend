# Opis Wykresów - Analiza Ratingów z Ankiet

## Wprowadzenie

Niniejszy dokument opisuje wszystkie wykresy generowane w ramach analizy ratingów z ankiet dotyczących oceny różnych wersji artykułów. Analiza obejmuje dwa typy ankiet:
- **Single ratings**: Oceny pojedynczych artykułów (5 wymiarów jakości)
- **Compare ratings**: Porównania między trzema wersjami artykułów

### Trzy wersje artykułów:
1. **Dziecięca (krótka)** - `child_short`
2. **Dorosła (krótka)** - `adult_short`
3. **Dorosła (pełna)** - `adult_full`

---

## WYKRESY DLA SINGLE RATINGS (Oceny pojedynczych artykułów)

### 1. Wykres #1: Średnie ocen według typu artykułu
**Plik:** `single_avg_ratings_by_style.png`

#### Co przedstawia:
Wykres słupkowy grupowy pokazujący średnie wartości każdej z pięciu kategorii oceny dla każdego typu artykułu. Każdy słupek reprezentuje średnią ocenę w skali 1-5, z paskami błędów pokazującymi odchylenie standardowe.

#### Kategorie oceny:
- **Przejrzystość** (clarity) - jak jasny i zrozumiały jest tekst
- **Dopasowanie stylu** (styleMatch) - czy styl odpowiada oczekiwaniom
- **Struktura** (structure) - organizacja treści
- **Użyteczność** (usefulness) - praktyczna wartość informacji
- **Przyjemność czytania** (enjoyment) - subiektywne odczucie

#### Jak interpretować:
- **Wyższe słupki** = lepsze oceny w danej kategorii
- **Paski błędów** pokazują zmienność odpowiedzi (szersze = większe rozbieżności)
- **Porównanie między stylami** pozwala zidentyfikować mocne i słabe strony każdego typu artykułu
- **Linia przerywana na poziomie 3.0** oznacza neutralną ocenę (średnia skali)
- Wartości powyżej 3.0 są pozytywne, poniżej - negatywne

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- Który typ artykułu jest najlepiej oceniany ogólnie?
- W jakich wymiarach każdy styl ma przewagę?
- Czy są systematyczne różnice w ocenach między wersjami?

---

### 2. Wykres #4: Heatmapa wiek × styl
**Plik:** `single_heatmap_age_style.png`

#### Co przedstawia:
Heatmapa (mapa ciepła) pokazująca średnią ocenę (ze wszystkich kategorii) dla każdej kombinacji grupy wiekowej i typu artykułu. Kolory reprezentują wartości: ciemniejsze/zielone = wyższe oceny, jaśniejsze/czerwone = niższe oceny.

#### Grupy wiekowe:
- 1-10 lat
- 11-20 lat
- 21-30 lat
- 31-40 lat
- 41-50 lat
- 51-60 lat
- 60+ lat

#### Jak interpretować:
- **Ciemniejsze/zielone komórki** = wyższe średnie oceny dla danej kombinacji wiek-styl
- **Jaśniejsze/czerwone komórki** = niższe oceny
- **Wartości w komórkach** pokazują dokładną średnią i liczbę odpowiedzi (n)
- **Wzorce poziome** (wzdłuż wierszy) pokazują preferencje danej grupy wiekowej
- **Wzorce pionowe** (wzdłuż kolumn) pokazują jak dany styl jest oceniany przez różne grupy

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- Czy młodsze grupy wiekowe preferują wersję dziecięcą?
- Czy starsze grupy lepiej oceniają wersję pełną?
- Czy istnieje interakcja między wiekiem czytelnika a typem treści?
- Czy artykuły trafiają do właściwej grupy docelowej?

---

### 3. Wykres S-D: Postrzeganie długości artykułów
**Plik:** `single_length_perception_stacked.png`

#### Co przedstawia:
Wykres słupkowy skumulowany (stacked bar chart) pokazujący rozkład procentowy ocen długości dla każdego typu artykułu. Każdy słupek sumuje się do 100% i pokazuje proporcje trzech kategorii oceny długości.

#### Kategorie oceny długości:
- **Za krótki** (too_short) - pomarańczowy
- **W sam raz** (just_right) - zielony
- **Za długi** (too_long) - czerwony

#### Jak interpretować:
- **Większy udział zielonego** = optymalna długość postrzegana przez większość
- **Dużo czerwonego** = artykuł jest postrzegany jako za długi
- **Dużo pomarańczowego** = artykuł jest postrzegany jako za krótki
- **Procenty na słupkach** pokazują dokładny rozkład odpowiedzi
- Idealnie: większość powinna być "w sam raz"

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- Czy wersja pełna (adult_full) jest faktycznie postrzegana jako za długa?
- Czy wersje krótkie są odpowiednio zbalansowane?
- Czy długość artykułów odpowiada oczekiwaniom czytelników?
- Która wersja ma najlepszą długość z perspektywy użytkownika?

---

## WYKRESY DLA COMPARE RATINGS (Porównania między wersjami)

### 4. Wykres #7: Zwycięstwa według kategorii
**Plik:** `compare_wins_by_category.png`

#### Co przedstawia:
Wykres słupkowy grupowy pokazujący liczbę zwycięstw (wyborów jako najlepsza) każdego typu artykułu w każdej z pięciu kategorii porównania.

#### Kategorie porównania:
1. **Najlepsza ogólnie** (bestOverall) - ogólna preferencja
2. **Najłatwiejsza do zrozumienia** (easiestToUnderstand) - przejrzystość
3. **Najlepsza dla dzieci** (bestForChildren) - przystępność dla młodych
4. **Najlepsza na szybki przegląd** (bestForQuickLook) - użyteczność do szybkiego czytania
5. **Najlepsza do planowania** (bestForPlanning) - wartość dla planowania działań

#### Jak interpretować:
- **Wyższe słupki** = więcej respondentów wybrało ten styl jako najlepszy w danej kategorii
- **Porównanie między kategoriami** pokazuje mocne strony każdego stylu
- **Wartości na słupkach** pokazują dokładną liczbę wyborów
- W każdej kategorii suma wszystkich słupków = liczba respondentów

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- W jakich kategoriach każdy styl ma przewagę?
- Czy wersja dziecięca rzeczywiście wygrywa w kategorii "dla dzieci"?
- Która wersja jest najlepsza do różnych celów użytkowania?
- Czy są systematyczne wzorce w wyborach?

---

### 5. Wykres #8: Najlepsza wersja ogólnie (Pie Chart)
**Plik:** `compare_best_overall_pie.png`

#### Co przedstawia:
Wykres kołowy (pie chart) pokazujący rozkład odpowiedzi na pytanie "Która wersja artykułu jest najlepsza ogólnie?". Każdy wycinek reprezentuje procent respondentów, którzy wybrali dany typ artykułu.

#### Jak interpretować:
- **Większy wycinek** = więcej głosów na ten typ artykułu
- **Procenty i liczby** pokazują dokładny rozkład preferencji
- **Wyróżniony wycinek** (lekko wysunięty) to zwycięzca
- Suma wszystkich wycinków = 100% respondentów

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- Która wersja jest najczęściej wybierana jako najlepsza ogólnie?
- Jaki jest rozkład preferencji między wersjami?
- Czy istnieje wyraźny faworyt, czy preferencje są podzielone?
- Czy wersja dziecięca, krótka czy pełna jest preferowana?

---

### 6. Wykres #9: Preferencje według grupy wiekowej
**Plik:** `compare_preferences_by_age_stacked.png`

#### Co przedstawia:
Wykres słupkowy skumulowany pokazujący rozkład preferencji "najlepsza wersja ogólnie" według grup wiekowych. Każdy słupek reprezentuje jedną grupę wiekową i sumuje się do 100%.

#### Jak interpretować:
- **Wysokość segmentu** w każdym słupku = procent wyborów danego stylu w danej grupie wiekowej
- **Porównanie między słupkami** pokazuje różnice preferencji między grupami wiekowymi
- **Procenty na segmentach** pokazują dokładny rozkład
- **Liczba w nawiasach (n=...)** pod każdym słupkiem = liczba respondentów w danej grupie

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- Czy młodsze grupy preferują wersję dziecięcą?
- Czy starsze grupy preferują wersję pełną?
- Czy preferencje zmieniają się z wiekiem?
- Czy artykuły trafiają do właściwej grupy docelowej?
- Czy istnieje korelacja między wiekiem a preferowanym stylem?

---

### 7. Wykres C-C: Konsensus per kategoria
**Plik:** `compare_consensus.png`

#### Co przedstawia:
Wykres słupkowy pokazujący procent respondentów, którzy wybrali "zwycięzcę" (najczęściej wybierany styl) w każdej kategorii. Mierzy siłę konsensusu - czy opinie są zgodne czy podzielone.

#### Jak interpretować:
- **Wysokie słupki** (>50%) = duży konsensus, jeden styl wyraźnie wygrywa
- **Niskie słupki** (<40%) = opinie podzielone, różne style mają podobne wyniki
- **Linia przerywana na 33%** = równy podział między 3 style (brak konsensusu)
- **Linia przerywana na 50%** = większość wybiera jeden styl
- **Kolor słupka** pokazuje który styl wygrał w danej kategorii
- **Wartości na słupkach** pokazują procent i nazwę zwycięzcy

#### Co oznacza dla pracy:
Wykres pozwala odpowiedzieć na pytania:
- W której kategorii jest największa zgodność opinii?
- W której kategorii opinie są najbardziej podzielone?
- Czy respondenci mają wyraźne preferencje, czy są niezdecydowani?
- Które kategorie generują największy konsensus?
- Czy niektóre kategorie są bardziej kontrowersyjne niż inne?

---

## Podsumowanie

### Wykresy Single Ratings (3 wykresy):
1. **Średnie ocen** - ogólna jakość każdego stylu w różnych wymiarach
2. **Heatmapa wiek × styl** - interakcja między wiekiem a preferencjami
3. **Postrzeganie długości** - ocena długości każdej wersji

### Wykresy Compare Ratings (4 wykresy):
1. **Zwycięstwa według kategorii** - mocne strony każdego stylu
2. **Najlepsza ogólnie (pie)** - ogólna preferencja
3. **Preferencje według wieku** - zależność wieku od wyboru
4. **Konsensus** - zgodność opinii w różnych kategoriach

### Kluczowe wnioski do wyciągnięcia:
- Która wersja artykułu jest najlepiej oceniana?
- Czy wersje trafiają do właściwych grup docelowych?
- W jakich kontekstach każda wersja ma przewagę?
- Czy długość artykułów jest odpowiednia?
- Czy istnieją systematyczne różnice między grupami wiekowymi?

---

## Uwagi techniczne

- Wszystkie wykresy generowane są w formacie PNG z rozdzielczością 300 DPI
- Kolory są spójne między wykresami (zielony = dziecięca, niebieski = dorosła krótka, fioletowy = dorosła pełna)
- Wykresy używają polskich etykiet i opisów
- Statystyki opisowe (średnie, odchylenia, liczności) są wyświetlane w konsoli przy generowaniu


