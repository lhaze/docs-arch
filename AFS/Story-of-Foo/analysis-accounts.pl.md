### Analiza domenowa

- [Domena: Konta](#domena-konta)

# Domena: Konta

## 1. Jakie pojęcia w systemie przekładają się na produkty?

- Konto:
  - opłata za konto
  - opłata za produkty powiązane (np. dopuszczalne saldo debetowe)
- Przelew:
  - prowizja za przelew
  - prowizja za przyspieszoną realizację przelewu
  - prowizja za przewalutowanie
- Produkt sprzedażowy:
  - pożyczka gotówkowa, zaproponowana przez real-time marketing po wykonaniu przelewu z tytułem „Na samochód”, etc.
  - karta powiązana z kontem

## 2. Na jakie pytania odpowiada system w odniesieniu do tych produktów?

- Ile mam środków?
- Jaka waluta?
- Czy posiadanie konta umożliwia mi dostęp do platformy bankowości elektronicznej?

2. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań? Zdarzenia są tu w rozumieniu zdarzenia domenowego: zmiany stanu procesu biznesowego, zmiany zachowania danego pojęcia, przemianę pojęcia w inne pojęcie. Nie: kliknięcie w guzik "Dalej" w jakimś interfejsie, ani nie zmianę jakiegoś stringa w jakiejś bazie.

3. Jakie są relacje między tymi zdarzeniami? Większość zdarzeń układa się w mniej lub bardziej regularne grupy, gdzie zachodzi np.:

               - następstwo w czasie albo skutkach,

               - uwspólnianie zdarzeń między różnymi procesami,

               - alternatywne ścieżki procesu,

               - alternatywne wejścia do procesu,

               - przerwy między zdarzeniami w czasie lub przestrzeni (w systemie lub organizacji)

Dobrym narzędziem do poszukiwań odpowiedzi na to pytanie jest Big Picture Event Storming. To technika warsztatowa, koordynująca wymianę wiedzy i szukanie wiarygodnych kandydatów na poddomeny w możliwie skondensowany i empiryczny sposób, bez wchodzenia w niepotrzebne szczegóły techniczne (3)

5. Te grupy zdarzeń domenowych stają się naturalnymi kandydatami na poddomeny. Kolejne propozycje na poddomeny to np. zakres kompetencji konkretnego analityka, bądź zespołu, pracującego w tej domenie. Struktura organizacyjna banku może być źródłem wiedzy o poddomenach, ale równie dobrze może oddawać nieaktualny albo nigdy będący procesowo optymalnym podział organizacji na silosy. Typowym nieoptymalnym podziałem są silosy ze względu na kompetencje z procesu zatrudnienia: programiści vs admini vs analitycy systemowi vs analitycy biznesowi.

6. Tu kończy się przeszukiwanie przestrzeni problemu, a zaczyna szukanie modelu rozwiązania. Domyślnie, każda z poddomen staje się tzw. bounded contextem. Kontekst jest "bounded", bo związany jest modelem (opisem pojęciami, którym nadajemy ścisłe znaczenie) z jakąś poddomeną, w której te znaczenia mają sens dla biznesu. Posiadanie kontekstów jeden do jednego może jednak być przesadnie dokładne i przez to niekorzystne, dlatego w dalszych krokach szukamy uproszczeń.

7. Czy któryś kontekstów da się zredukować przez usunięcie niepotrzebnych szczegółów? Opis poddomeny może zawierać elementy nieistotne ze względu na jej zbiór zdarzeń domenowych. Uogólnienie przez usunięcie nieistotnych szczegółów może doprowadzić do prostszego systemu i uwspólnienia bounded contextów różnych poddomen.

8. Czy dany konktest zawiera w sobie wszystkie informacje, konieczne do odpowiedzi na całe pytanie i obsługi wszystkich zdarzeń jego poddomeny? Czy może czegoś krytycznego brakuje i trzeba zespolić go z innym kontekstem?

9. Czy każde pytanie domenowe ma bounded context, który jest dla niego pojedynczym źródłem prawdy? Czy nie będzie sytuacji, że żeby przejść jakiś proces, trzeba odpytać 10 mikroserwisów, żeby dowiedzieć się o że coś jest możliwe? Gdy dziesiąta odpowiedź wróci to pierwsza będzie nieaktualna?

10. Czy dany kontekst nie próbuje posiadać danych i/lub odpowiedzialności, które nie są konieczne do odpowiedzi na pytania, które są jego celem? Tzw. data/feature envy jest szybką drogą do zgubienia niezależności miedzy kandydatami na mikroserwisy.

11. Które poddomeny są strategiczne, tj. odpowiadające za kluczowe cechy produktu i będące źródłem jego przewagi? Te w szczególności mogą potrzebować własnego bounded contextu, bo tam jest duża szansa na pojawianie się zmian w oczekiwaniach biznesowych i potrzebę szybkiej adaptacji. Pozostałe poddomeny mogą dostawać ze strony organizacji mniejszą uwagę, a niektóre być na tyle typowe, rzadko zmienne albo mało istotne, że będzie zupełnie akceptowalne, że są realizowane przez systemy legacy albo "na piechotę".

12. Strategiczne bounded contexty stają się naturalnym kandydatem do realizacji jako moduły (w rozumieniu architektury aplikacyjnej) i mieć swoją implementację w jakimś repozytorium.

13. Czy któreś bounded contexty są źródłem podatności systemu na częste zmiany? Albo są chaotyczne, trudne do zanalizowania? Mają specjalne potrzeby techniczne, np. bardzo wysoką dostępność? A może potrzebujemy oddać taki kontekst jakiemuś konkretnemu zespołowi ze względu na podział pracy albo trudność w znalezieniu developerów? Takie szczególne cechy kontekstu wskazują na potrzebę umieszczenia go w wyodrębnionym module, aby nie zaburzać rytmu rozwoju pozostałych modułów.

14. Na jakimś etapie realizacji, decydujemy o modelu wdrożeniowym. Częsci modułów o dobrze określonych granicach ich bounded contextu nadajemy charakter mikroserwisu:

               - tym które mają często zmienną logikę biznesową,

               - tym które mają wymaganie wysokiej high availability,

               - tym które w szczególny sposób muszą mieć dostrojony model wdrożeniowy ze względu na normy ISO/polityki bezpieczeństwa.

Dopiero na tym etapie jest sens zastanawiać się nad szczegółami takimi jak np. Kubernetes vs ARO, czy chmura czy on-premise.

15. Czasem świadomie możemy nie chcieć wydzielać mikroserwisów z modułów, np. gdy:

               - nie jesteśmy jeszcze pewni granic bounded contextów dookoła takiego modułu

               - gdy jest to związane z niedekomponowalnym systemem legacy, od którego kontekst zależy.

Ostatecznie, zdekomponowany na moduły, ale nie wdrożony w mikroserwisy, monolit też zapewnia część cech oczkekiwanych przez R2C:

               - skalowalność: moduły o dobrze określonych granicach, też można zwielokrotnić całością monolitu i włączać/wyłączać feature-flagami; kosztem jest jedynie pamięć operacyjna,

               - niezależność rozwoju: monolit nie musi koniecznie pochodzić z mono-repozytorium, może dawać zespołom niezależność developmentu, choć nie zabezpieczoną fizycznymi granicami maszyny, na której to jest uruchomione, jak w przypadku mikroserwisów,

               - hermetyzację: komunikacja z innymi modułami tylko na podstawie dobrze określonego i stabilnego kontraktu,

               - podatność na eksperymenty: możliwość ułatwienia sprawdzania innych rozwiązań i wykonania jakiegoś pivotu biznesowego czy technicznego,

... tylko niezależności wdrożeniowej nie posiada --- wciąż będzie podatny na wdrożenia jako wielkie święto i duże ryzyko.
