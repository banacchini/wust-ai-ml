# Audyt kompletnosci notebooka `01_data_processing.ipynb` wzgledem polecenia

## Zakres oceny
Ocena obejmuje:
- zgodnosc z sekcja "Przebieg cwiczenia" (pkt 1-5),
- zgodnosc z kryteriami punktacji (max 10 pkt),
- jakosc odpowiedzi na pytania dodatkowe,
- ogolna jakosc merytoryczna i techniczna rozwiazania.

---

## 1) Ocena podpunktow z polecenia (Przebieg cwiczenia)

### 1. Badanie cech zbioru wraz z wizualizacja
**Status:** wykonane bardzo dobrze  
**Dowody:**
- analiza rozkladu klas,
- rekonstrukcja osi czasu (`years_to_prediction`) i analiza po horyzoncie,
- analiza brakow danych (globalnie, per year, per klasa),
- liczne wykresy (countplot, boxplot, violinplot, histogram).

**Uwagi:**
- EDA jest bogata i przekracza minimum zadania.

### 2. PCA + wizualizacja + analiza wynikow
**Status:** wykonane dobrze  
**Dowody:**
- PCA 2D na train,
- raport wyjasnionej wariancji,
- wykres PCA,
- dodatkowo analiza loadingow (najwazniejsze cechy dla PC1/PC2).

**Uwagi:**
- bardzo dobry element ponadstandardowy: interpretacja loadingow.

### 3. t-SNE + wizualizacja + analiza wynikow
**Status:** wykonane dobrze  
**Dowody:**
- t-SNE na podprobce train,
- sampling stratyfikowany,
- wykres i porownanie wizualne.

**Uwagi:**
- poprawne podejscie obliczeniowe i metodyczne.

### 4. Preprocessing (braki danych, skala, outliery) + porownanie metod
**Status:** wykonane bardzo dobrze (z 1 istotna niespojnoscia opisowa)  
**Dowody:**
- porownanie 3 strategii missing-data,
- porownanie 3 strategii outlierow (winsoryzacja),
- porownanie 3 skalerow,
- anty-leakage (fit na train, transform na test),
- benchmark kombinacji i wybor najlepszej konfiguracji.

**Niespojnosc:**
- w czesci odpowiedzi opisowej pojawia sie odniesienie do Isolation Forest, ale glowny pipeline stosuje winsoryzacje, nie detekcje IF. To warto ujednolicic.

### 5. Podzial train/test + 2 modele klasyfikacji + analiza wynikow
**Status:** wykonane bardzo dobrze  
**Dowody:**
- jawny split przed fitowaniem transformacji,
- stratyfikacja (z fallbackiem),
- dwa modele: RandomForest + LogisticRegression,
- metryki, classification report, macierze pomylek,
- dodatkowe porownania konfiguracji.

---

## 2) Ocena wg kryteriow punktowych (max 10)

1. Analiza zbioru danych - wizualizacja (2 pkt): **2/2**  
2. PCA + wizualizacja (1 pkt): **1/1**  
3. t-SNE + wizualizacja (1 pkt): **1/1**  
4. Czyszczenie zbioru + skale + outliery + analiza (4 pkt): **4/4**  
5. Dwa algorytmy + analiza wynikow (2 pkt): **2/2**

**Suma szacunkowa: 10/10**

Komentarz: formalnie i praktycznie notebook pokrywa komplet wymaganych elementow, a nawet wykracza poza minimum.

---

## 3) Ocena pytan dodatkowych (sekcja koncowa)

### Pytanie 1 (PCA)
**Status:** odpowiedz jest, merytorycznie poprawna.

### Pytanie 2 (t-SNE i roznica vs PCA)
**Status:** odpowiedz jest, merytorycznie poprawna.

### Pytanie 3 (standaryzacja vs normalizacja)
**Status:** odpowiedz jest, sensowna.

### Pytanie 4 (outliery + wplyw na split)
**Status:** czesciowo do poprawy.

**Dlaczego:**
- opis miesza podejscia (wspomniany Isolation Forest) z tym, co faktycznie zrobiono w pipeline (winsoryzacja).
- warto jednoznacznie opisac "wybrana metode" zgodnie z implementacja.

### Pytanie 5 (wybrane metody klasyfikacji)
**Status:** odpowiedz jest i pokrywa oba modele.

---

## 4) Najwazniejsze poprawki do wdrozenia

1. Ujednolicic narracje o outlierach
- W pytaniu 4 i komentarzach wpisac jasno, ze praktycznie testowano winsoryzacje (`q1-q99` i `IQR`), a nie Isolation Forest.

2. Dodac krotka sekcje "Finalne wnioski"
- 5-8 punktow: najlepsza konfiguracja, kompromis precision/recall/F2, co daje najwiekszy zysk.
- To ulatwi ocene raportu przez prowadzacego.

3. Ograniczyc czesci poboczne do dodatku
- Sekcje "Appendix" i eksperymenty relacyjne sa wartosciowe, ale glowny tor rozwiazania powinien byc wyraznie oddzielony od rozszerzen.

4. Zwiekszyc reprodukowalnosc
- Dodac jedna komorke "Run order / seed setup" na poczatku (jeden punkt odniesienia, wszystkie random_state i ustawienia).

5. Uporzadkowac jezyk komentarzy
- Jest bardzo duzo tresci i miejscami styl jest nierowny (od formalnego po potoczny). Krotka redakcja podniesie jakosc raportowa.

---

## 5) Ogolna ocena jakosci rozwiazania

**Ocena ogolna: bardzo wysoka (ok. 9/10).**

Mocne strony:
- bardzo dobra kompletnosc wzgledem polecenia,
- poprawna metodologia anti-leakage,
- szerokie porownanie wariantow preprocessingu,
- solidna ewaluacja modeli i czytelne wizualizacje,
- elementy ponadprogramowe (duplikaty, mechanistic missingness, dodatkowe benchmarki).

Ryzyka/slabsze punkty:
- niespojnosc opisu metody outlierowej w odpowiedzi teoretycznej,
- nadmiar eksperymentow moze utrudnic szybka ocene prowadzacemu,
- brakuje zwartego finalnego podsumowania decyzyjnego.

Wniosek koncowy: rozwiazanie jest merytorycznie mocne i praktycznie kompletne; po drobnych poprawkach redakcyjnych bedzie bardzo dobre takze w odbiorze raportowym.
