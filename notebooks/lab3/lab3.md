# Uczenie Maszynowe. Laboratorium 2

### Modele liniowe: regresja liniowa i logistyczna

### Oleksii Furman Przemysław Dolata

### Data aktualizacji: 26.03.

## 1 Cel ćwiczenia

Celem ćwiczenia jest zrozumienie fundamentów uczenia maszynowego poprzez analizę modeli
liniowych. W przeciwieństwie do algorytmów „czarnej skrzynki”, modele te oferują wysoką inter-
pretowalność.
Zapoznasz się z problemem regresji (przewidywanie wartości ciągłej) oraz klasyfikacji
(przewidywanie etykiety) w ujęciu geometrycznym. Kluczowym aspektem będzie zbadanie wpływu
regularyzacji na „złożoność” modelu (bias-variance tradeoff).
Dla studentów chcących zgłębić temat, przygotowano zadanie dodatkowe z Maszyn Wek-
torów Nośnych (SVM).

## 2 Wprowadzenie

### 2.1 Od linii do decyzji

Wiele problemów można sprowadzić do znalezienia optymalnej hiperpłaszczyzny (linii w 2D)
w wielowymiarowej przestrzeni cech.

- Regresja liniowa: Próbuje dopasować n-wymiarową linię tak, aby zminimalizować błąd
    (np. sumę kwadratów różnic między predykcją a rzeczywistością).

```
y = w 1 x 1 + ... + wnxn+ b
```
- Regresja logistyczna: Mimo nazwy, jest to klasyfikator. Wynik równania liniowego jest
    transformowany przez funkcję sigmoidalną, co pozwala interpretować wyjście jako praw-
    dopodobieństwo przynależności do klasy.

### 2.2 Problem przeuczenia i regularyzacja

Gdy model zbyt mocno dopasuje się do danych treningowych (w tym szumu), mamy do czynienia
z przeuczeniem (overfitting). Rozwiązaniem jest dodanie kary za „wielkość” wag modelu.

```
Koszt = Błąd (MSE) + α· Kara za wielkość wag
```
- Ridge (L2): Preferuje małe, rozproszone wagi.
- Lasso (L1): Preferuje wagi zerowe (działa jak automatyczna selekcja cech).


## 3 Użyte zbiory danych

W ćwiczeniu wykorzystamy zbiory znane z poprzednich laboratoriów:

1. WINE (dostępny w sklearn): Tym razem nie będziemy tylko klasyfikować odmian wina.
    Spróbujemy przewidzieć zawartość konkretnego składnika chemicznego (np. alcohol lub
    magnesium) na podstawie pozostałych cech (zadanie regresji).
2. Polish Companies Bankruptcy (z Lab 1): Zbiór trudny, niezbalansowany, idealny do
    testowania regresji logistycznej.

## 4 Przebieg ćwiczenia

### 4.1 Zadanie 1: Regresja i regularyzacja (zbiór WINE)

1. Załaduj zbiór WINE. Wybierz jedną z cech ciągłych jako cel (np. alcohol), a pozostałe
    pozostaw jako cechy.
2. Podziel zbiór na treningowy i testowy.
3. Uruchom regresję liniową, korzystając z sklearn.LinearRegression.
4. Oblicz metryki R^2 oraz MSE (Mean Squared Error) na obu podzbiorach.
5. Zastosuj modele z regularyzacją: Ridge i LASSO.
    - Sprawdź wpływ parametru α na wyniki.
    - Eksperyment: Utwórz wykres, gdzie na osi X będzie wartość α (skala logarytmiczna),
       a na osi Y wartości współczynników (wag) modelu. Zaobserwuj, jak LASSO „zeruje”
       mniej istotne cechy, dokonując selekcji zmiennych.
6. Wykorzystaj walidację krzyżową do wyznaczenia optymalnej wartości α.
    - Porównaj wynik uzyskany przy ręcznie dobranym α z wynikiem zaproponowanym
       przez walidację krzyżową.
    - Zastanów się, dlaczego ewaluacja modelu na pojedynczym podziale train/test może
       dawać niestabilne oszacowanie jakości i jak k-fold CV temu zapobiega.

### 4.2 Zadanie 2: Klasyfikacja probabilistyczna (zbiór Bankruptcy)

1. Załaduj zbiór danych o bankructwie (wybierz jeden rok, np. 3year.arff).
2. Uruchom regresję logistyczną za pomocą sklearn.LogisticRegression.
    - Uwaga: Modele liniowe są wrażliwe na skalę danych. Użycie StandardScaler jest
       obowiązkowe!
3. Wyniki przedstaw w postaci macierzy pomyłek (confusion matrix) oraz wyliczonych na
    ich podstawie najistotniejszych metryk (np. precyzja, czułość). Liczy się też umiejętność
    wyjaśnienia co znaczą te metryki!
    Zinterpretuj wyniki:
       - Które cechy (wskaźniki finansowe) mają największe dodatnie, a które ujemne wagi?
          Czy ma to sens ekonomiczny?
       - Jak zmienią się wartości metryk, gdy zmodyfikujemy próg klasyfikacji?


4. Zbadaj zachowanie modelu przy różnych wartościach parametru regularyzacji C. Porównaj
    działanie regularyzacji Ridge i LASSO (parametr l1_ratio).
    Wariant regularyzacji Elastic Net możesz również przebadać, ale wyniki tego podejścia będą
    sprawdzane wyłącznie wtedy, gdy pochwalisz się dostatecznym zrozumieniem teoretycznym
    metody.

### 4.3 Zadanie 3 [Dla chętnych]: Geometria SVM

SVM to algorytm szukający najszerszego „marginesu” między klasami w przestrzeni danych.

1. Uruchom klasyfikator SVM (Support Vector Machine, w sklearn nazywany też SVC
    od Support Vector Classifier) z jądrem liniowym (kernel=’linear’) na zbiorze Bankruptcy
    lub WINE (klasyfikacja).
2. Porównaj go z jądrem RBF (kernel=’rbf’). Czy nieliniowość (zakrzywienie przestrzeni)
    poprawia wynik?
3. Wizualizacja: Wybierz tylko 2 cechy ze zbioru i narysuj granice decyzyjne (decision bo-
    undaries) dla SVM.

## 5 Punktacja

Przy realizacji zadania możesz otrzymać max 8 punktów wedle poniższej tabeli:

```
Pkt Zadanie
4 Regresja liniowa: Poprawne przeprowadzenie regresji, oblicze-
nie błędów (MSE, R^2 ) i wizualizacja zanikania współczynników
w LASSO/Ridge (ścieżka regularyzacji).
4 Regresja logistyczna: Poprawne przeprowadzenie procesu (podział da-
nych, skalowanie, uczenie i testowanie modelu), wyliczenie i interpre-
tacja metryk jakości oraz wag modelu (wskazanie najważniejszych cech
wpływających na decyzję), badanie parametru regularyzacji.
```
- [Opcjonalnie] SVM: Porównanie jądra liniowego i RBF. Analiza
    wpływu parametru C (koszt) na margines decyzyjny.

## 6 Pytania pomocnicze

1. Dlaczego skalowanie danych (np. StandardScaler) jest krytyczne dla Lasso/Ridge, a mniej
    ważne dla Drzew Decyzyjnych?
2. Czym różni się minimalizowanie błędu L 1 od L 2?
3. Dlaczego w przypadku niezbalansowanego zbioru (Bankruptcy) „surowa” celność (Accu-
    racy) regresji logistycznej może być myląca? Co nam daje analiza progu prawdopodobień-
    stwa?
4. [Do zadania z SVM]: Co oznacza, że punkt jest „wektorem nośnym”?


## 7 Literatura

1. Linear Models (scikit-learn): https://scikit-learn.org/stable/modules/linear_model.
    html
2. Regularization (Ridge/Lasso): https://scikit-learn.org/stable/auto_examples/linear_
    model/plot_ridge_path.html
3. Cichosz P. „Systemy uczące się”, WNT Warszawa (Rozdziały o modelach liniowych).


