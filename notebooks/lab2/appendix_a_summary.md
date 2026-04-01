# Appendix A - podsumowanie i zasady kwalifikacji relacji do imputacji

## Cel Appendixu A
Appendix A sprawdza, czy brakujace wartosci w cechach A1..A64 da sie wiarygodnie uzupelniac przez relacje algebraiczne miedzy atrybutami (exact-candidates), zamiast imputowac je tylko statystycznie (np. mediana).

Sekcja robi to w 4 krokach:
1. Waliduje kandydatow relacji na danych rzeczywistych.
2. Wybiera tylko relacje, ktore przechodza surowe progi jakosci.
3. Buduje slownik relacji gotowych do ewentualnej imputacji.
4. Pokazuje diagnostyke: ile pol da sie uzupelnic one-shot i co blokuje pozostale przypadki.

## Jak liczona jest jakosc relacji
Dla kazdej relacji najpierw wyznaczany jest zbior wierszy, na ktorych relacja moze byc policzona:
- wszystkie wejscia relacji musza byc nie-NaN,
- musza byc spelnione guardy (np. nonzero dla mianownika),
- target w walidacji musi byc znany (nie-NaN), zeby policzyc blad.

Nastepnie liczone sa metryki:
- MAE,
- median MAPE (%),
- p95 MAPE (%),
- R2,
- coverage (%): udzial wierszy z policzalna relacja wsrod wierszy, gdzie target jest znany.

Dodatkowo raportowany jest imputable_missing_count, czyli ile brakow targetu relacja potencjalnie moze uzupelnic.

## Kryteria PASS (kwalifikacja relacji)
Relacja jest uznana za odpowiednia do imputacji tylko wtedy, gdy spelnia wszystkie warunki:
1. median MAPE <= 0.5%
2. p95 MAPE <= 2.0%
3. coverage >= 80%
4. median MAPE i p95 MAPE sa zdefiniowane (nie-NaN)

Progi sa pobierane ze strict_thresholds.

W praktyce to oznacza, ze relacja musi byc jednoczesnie:
- dokladna typowo (mediana bledu),
- odporna na ogony bledu (p95),
- wystarczajaco szeroko stosowalna (coverage),
- a nie tylko przypadkowo dobra na malym podzbiorze.

## Dodatkowy filtr bezpieczenstwa przed zapisem slownika
Po walidacji robiony jest jeszcze jeden check (threshold_mask) na tych samych progach.
Do slownika exact_relations_for_imputation.json trafiaja tylko relacje, ktore:
- maja pass == True,
- dalej przechodza reczna kontrole progow,
- istnieja w pliku relacji zrodlowych.

To jest celowe zdublowanie kontroli, zeby uniknac przypadkowego przepuszczenia relacji po zmianach danych/plikow.

## Jak potem wykonywana jest imputacja
Imputacja relacyjna jest wykonywana tylko dla relacji PASS:
- grupowanie po target_attr,
- kolejnosc uzycia relacji: priority, potem nizsze p95 MAPE i median MAPE,
- uzupelnianie tylko tam, gdzie target jest NaN i relacja jest policzalna.

Dzieki temu najpierw probowane sa relacje najbardziej wiarygodne dla danego targetu.

## One-shot i diagnostyka blokad
W kolejnych komorkach sprawdzany jest tryb one-shot:
- predykcje liczone na bazowym stanie danych (bez iteracyjnego propagowania nowych wartosci),
- raport: ile pol i wierszy jest realnie uzupelnialnych jednym przebiegiem.

Potem diagnostyka rozdziela przyczyny braku imputacji na:
- brak wejsc relacji,
- niespelnione guardy,
- oba naraz.

To pokazuje, czy glowna bariera jest strukturalna (guardy), czy informacyjna (braki wejsc).

## Wniosek
Kwalifikacja relacji w Appendixie A jest rygorystyczna i wieloetapowa:
- najpierw walidacja numeryczna na znanych wartosciach,
- potem surowe progi dokladnosci i pokrycia,
- na koncu dodatkowy filtr bezpieczenstwa przy zapisie slownika.

Dzieki temu relacje dopuszczane do imputacji to tylko te, ktore sa jednoczesnie dokladne i praktycznie uzyteczne.