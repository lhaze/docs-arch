### Analiza domenowa

- [Opis procedury analizy](#opis-procedury-analizy)
  - [1. Jakie pojęcia w systemie przekładają się na produkty?](#1-jakie-pojęcia-w-systemie-przekładają-się-na-produkty)
  - [2. Na jakie pytania odpowiada system w odniesieniu do tych produktów?](#2-na-jakie-pytania-odpowiada-system-w-odniesieniu-do-tych-produktów)
  - [3. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań?](#3-jakie-zdarzenia-wpływają-na-zmianę-odpowiedzi-na-każde-z-tych-pytań)
  - [4. Jakie są relacje między tymi zdarzeniami?](#4-jakie-są-relacje-między-tymi-zdarzeniami)
  - [5. Wyłanianie kandydatów na poddomeny](#5-wyłanianie-kandydatów-na-poddomeny)
  - [6. Czy potencjalne poddomeny są istotnie różne?](#6-czy-potencjalne-poddomeny-są-istotnie-różne)
  - [7. Wyłanianie kandydatów na bounded contexty](#7-wyłanianie-kandydatów-na-bounded-contexty)
  - [8. Czy któryś kontekstów da się zredukować przez usunięcie niepotrzebnych szczegółów?](#8-czy-któryś-kontekstów-da-się-zredukować-przez-usunięcie-niepotrzebnych-szczegółów)
  - [9. Czy dany kontekst zawiera w sobie wszystkie konieczne informacje?](#9-czy-dany-kontekst-zawiera-w-sobie-wszystkie-konieczne-informacje)
  - [10. Czy każde pytanie domenowe ma bounded context, który jest dla niego pojedynczym źródłem prawdy?](#10-czy-każde-pytanie-domenowe-ma-bounded-context-który-jest-dla-niego-pojedynczym-źródłem-prawdy)
  - [11. Czy dany kontekst nie próbuje posiadać danych i/lub odpowiedzialności, które nie są konieczne do odpowiedzi na pytania, które są jego celem?](#11-czy-dany-kontekst-nie-próbuje-posiadać-danych-ilub-odpowiedzialności-które-nie-są-konieczne-do-odpowiedzi-na-pytania-które-są-jego-celem)
  - [12. Które poddomeny są strategiczne?](#12-które-poddomeny-są-strategiczne)
  - [13. Wyłanianie kandydatów na moduły](#13-wyłanianie-kandydatów-na-moduły)
  - [14. Czy któreś bounded contexty są źródłem podatności systemu na częste zmiany?](#14-czy-któreś-bounded-contexty-są-źródłem-podatności-systemu-na-częste-zmiany)
  - [15. Wyłanianie kandydatów na mikroserwisy](#15-wyłanianie-kandydatów-na-mikroserwisy)

# Opis procedury analizy

## 1. Jakie pojęcia w systemie przekładają się na produkty?

- Jak najprostsze rozumienie pojęć:
  - System to rozwiązanie techniczne, mierzące się z jakimś problemem. System może być rozwiązaniem technicznym (oprogramowaniem lub usługą IT), ale może być rozwiązaniem organizacyjnym (zespołem). System będzie najwyższym piętrem abstrakcji rozwiązania (patrz: [C4 Model](https://c4model.com/)).
  - Produkt to coś, przynoszące klientowi jakąś korzyść, nadające się na cel istnienia systemu. Produkt oczywiście nie musi być materialny, może być usługą IT lub organizacyjną.
- Spośród wszystkich pojęć, jakimi system operuje, warto za początek analizy wziąć te, które przynoszą wartość.
- Głęboko fałszywe najczęściej okazuje się założenie, że można stworzyć wartościową architekturę IT, ignorując cel biznesowy, dla którego miała zostać stworzona. Założenia nie stoją w miejscu [...]

## 2. Na jakie pytania odpowiada system w odniesieniu do tych produktów?

- Zmiany, które przekraczają granice mikroserwisów są drogie i skomplikowane. Częste takie zmiany niweczą pierwotny cel architektury mikroserwisów: autonomiczność w działaniu i rozwoju.
- Celem tej procedury jest znalezienie takiego podziału rozwiązania technicznego, który optymalizowałby jego postać ze względu na potencjalne zmiany. Jest korzystne, aby inicjatywy do zmian - zarówno od strony biznesu, jak i techniczne - zawierały się wewnątrz możliwie małej ilości komponentów. W idealnym świecie, w jednym mikroserwisie.
- Metodą może być pójście za tropem problemów rozwiązywanych przez system i tego, które rozwiązania są źródłem wartości systemu dla klienta.
- Wszystkich potencjalnych pytań jest zbyt dużo, żeby rozważanie dało efektywne planowanie. Spośród nich, warto wybierać te, które wyciągają podstawowy sens istnienia systemu.

## 3. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań?

- Zdarzenia są tu w rozumieniu zdarzenia domenowego:
  - zmiany stanu procesu biznesowego,
  - zmiany zachowania danego pojęcia,
  - przemianę pojęcia w inne pojęcie.

- Nie są zdarzeniami domenowymi:
  - kliknięcie przycisku „Dalej” w jakimś interfejsie,
  - zmiana jakiegoś stringa w jakiejś bazie.

- Dobrmi kandydatami na zaczepkę są:
  - zdarzenie, które jest celem procesu, np. "Pieniądze trafiły na konto docelowe"
  - zdarzenie, będące kluczowym krokiem lub największym wyzwaniem do osiągnięcia celu, np. "Przelew został zarejestrowany w systemie centralnym"

- Złymi kandydatami są te, które odwołują się do struktury wewnętrznej pojęć, np. "zmieniono numer konta docelowego" albo "wybrano urząd skarbowy". Struktura wewnętrzna lub nawet same pojęcia mogą się zmieniać.

- Następne zdarzenia mogą być dookreślane przez szukanie źródła lub celu już znalezionych. Being, Behaving, Becoming ([*Rethinking Systems Analysis and Design*](https://leanpub.com/rethinkingsystemsanalysisanddesign), G. Weinberg)

  - Kiedy się stało?
  - Dlaczego?
  - Jakie rzeczy muszą się zdarzyć wcześniej?
  - Kto to zmienia?
  - Czy można to powtórzyć?
  - Czy można to wycofać?
  - Jak często się zmienia?

## 4. Jakie są relacje między tymi zdarzeniami?

- Większość zdarzeń układa się w mniej lub bardziej regularne grupy, gdzie zachodzi np.:
  - następstwo w czasie albo skutkach,
  - uwspólnianie zdarzeń między różnymi procesami,
  - alternatywne ścieżki procesu,
  - alternatywne wejścia do procesu,
  - przerwy między zdarzeniami w czasie lub przestrzeni (w systemie lub organizacji).

- Dobrym narzędziem do poszukiwań odpowiedzi na to pytanie jest Big Picture Event Storming. To technika warsztatowa, koordynująca wymianę wiedzy i szukanie wiarygodnych kandydatów na poddomeny w możliwie skondensowany i empiryczny sposób, bez wchodzenia w niepotrzebne szczegóły techniczne (3)

## 5. Wyłanianie kandydatów na poddomeny

Te grupy zdarzeń domenowych stają się naturalnymi kandydatami na poddomeny. Obecność grup może wskazywać na potrzebę jakiejś spójności (np. danych lub czasu), natomiast przerwy w procesie są naturalnymi kandydatami do rozdzielenia spójnością ostat

Kolejne propozycje na poddomeny to np. zakres kompetencji konkretnego analityka bądź zespołu, pracującego w tej domenie. Struktura organizacyjna może być źródłem wiedzy o poddomenach, ale równie dobrze może oddawać nieaktualny albo nieoptymalny podział organizacji na silosy. Typowym nieoptymalnym podziałem są silosy ze względu na kompetencje z procesu zatrudnienia pracownika: programiści kontra admini kontra analitycy systemowi kontra analitycy biznesowi.

## 6. Czy potencjalne poddomeny są istotnie różne?

- Analiza nie jest jednak tylko obserwacją powierzchniowych zdarzeń:

  - > Trzeba sobie tu jasno powiedzieć, że indukcyjne podejście do analizy (zbieranie i zapisywanie obserwacji w celu identyfikacji trendu lub powtórzeń) przypomina próby zrozumienia gry w szachy metodą wielokrotnej obserwacji rozgrywek. Im wierniejszy opis gry ma powstać, tym więcej obserwacji należy udokumentować, co nie zmienia faktu, że taki dokument nie mówi absolutnie nic o przyszłych rozgrywkach. Alternatywą jest dedukcyjne podejście, polegające na zrozumieniu i opracowaniu, możliwie najmniejszym nakładem pracy, reguł gry w szachy, czego udokumentowanie wymaga najwyżej dwóch stron papieru A4, taki dokument opisuje także w 100% wszystkie przyszłe rozgrywki…
      >
      > — J. Żeliński, [Biznesowy model danych — nie chcemy.](https://it-consulting.pl/autoinstalator/wordpress/2017/02/03/biznesowy-model-danych-nie-chcemy/)

  - Z listy wymagań, zbioru User Story czy zestawu makiet ekranów nie wynika [...]

## 7. Wyłanianie kandydatów na bounded contexty

- Tu kończy się przeszukiwanie przestrzeni problemu, a zaczyna szukanie modelu rozwiązania.
- Domyślnie, każda z poddomen staje się tzw. bounded contextem. Kontekst jest "bounded", bo związany jest modelem (opisem pojęciami, którym nadajemy ścisłe znaczenie) z jakąś poddomeną, w której te znaczenia mają sens dla biznesu. Posiadanie kontekstów jeden do jednego może jednak być przesadnie dokładne i przez to niekorzystne, dlatego w dalszych krokach szukamy uproszczeń.

## 8. Czy któryś kontekstów da się zredukować przez usunięcie niepotrzebnych szczegółów?

- Opis poddomeny może zawierać elementy nieistotne ze względu na jej zbiór zdarzeń domenowych. Uogólnienie przez usunięcie nieistotnych szczegółów może doprowadzić do prostszego systemu i uwspólnienia bounded contextów różnych poddomen.

## 9. Czy dany kontekst zawiera w sobie wszystkie konieczne informacje?

- konieczne do odpowiedzi na całe pytanie i obsługi wszystkich zdarzeń jego poddomeny?
- Czy może czegoś krytycznego brakuje i trzeba zespolić go z innym kontekstem?

## 10. Czy każde pytanie domenowe ma bounded context, który jest dla niego pojedynczym źródłem prawdy?

- Czy nie będzie sytuacji, że żeby przejść jakiś proces, trzeba odpytać 10 mikroserwisów, żeby dowiedzieć się o że coś jest możliwe? Gdy dziesiąta odpowiedź wróci to pierwsza będzie nieaktualna?

## 11. Czy dany kontekst nie próbuje posiadać danych i/lub odpowiedzialności, które nie są konieczne do odpowiedzi na pytania, które są jego celem?

- Tzw. data/feature envy jest szybką drogą do zgubienia niezależności miedzy kandydatami na mikroserwisy.

## 12. Które poddomeny są strategiczne?

- tj. odpowiadające za kluczowe cechy produktu i będące źródłem jego przewagi? Te w szczególności mogą potrzebować własnego bounded contextu, bo tam jest duża szansa na pojawianie się zmian w oczekiwaniach biznesowych i potrzebę szybkiej adaptacji. Pozostałe poddomeny mogą dostawać ze strony organizacji mniejszą uwagę, a niektóre być na tyle typowe, rzadko zmienne albo mało istotne, że będzie zupełnie akceptowalne, że są realizowane przez systemy legacy albo "na piechotę".

## 13. Wyłanianie kandydatów na moduły

- Strategiczne bounded contexty stają się naturalnym kandydatem do realizacji jako moduły (w rozumieniu architektury aplikacyjnej) i mieć swoją implementację w jakimś repozytorium.

## 14. Czy któreś bounded contexty są źródłem podatności systemu na częste zmiany?

Albo są chaotyczne, trudne do zanalizowania? Mają specjalne potrzeby techniczne, np. bardzo wysoką dostępność? A może potrzebujemy oddać taki kontekst jakiemuś konkretnemu zespołowi ze względu na podział pracy albo trudność w znalezieniu developerów? Takie szczególne cechy kontekstu wskazują na potrzebę umieszczenia go w wyodrębnionym module, aby nie zaburzać rytmu rozwoju pozostałych modułów.

## 15. Wyłanianie kandydatów na mikroserwisy

- Na jakimś etapie realizacji, decydujemy o modelu wdrożeniowym. Części modułów o dobrze określonych granicach ich bounded contextu nadajemy charakter mikroserwisu:

  - tym które mają często zmienną logikę biznesową,
  - tym które mają wymaganie wysokiej high availability,
  - tym które w szczególny sposób muszą mieć dostrojony model wdrożeniowy ze względu na normy ISO/polityki bezpieczeństwa.

- Dopiero na tym etapie jest sens zastanawiać się nad szczegółami takimi jak np. Kubernetes vs ARO, czy chmura czy on-premise.
- Czasem świadomie możemy nie chcieć wydzielać mikroserwisów z modułów, np. gdy:

- nie jesteśmy jeszcze pewni granic bounded contextów dookoła takiego modułu
- gdy jest to związane z niedekomponowalnym systemem legacy, od którego kontekst zależy.

- Ostatecznie, zdekomponowany na moduły, ale nie wdrożony w mikroserwisy, monolit też zapewnia część cech oczkekiwanych przez R2C:

  - skalowalność: moduły o dobrze określonych granicach, też można zwielokrotnić całością monolitu i włączać/wyłączać feature-flagami; kosztem jest jedynie pamięć operacyjna,
  - niezależność rozwoju: monolit nie musi koniecznie pochodzić z mono-repozytorium, może dawać zespołom niezależność developmentu, choć nie zabezpieczoną fizycznymi granicami maszyny, na której to jest uruchomione, jak w przypadku mikroserwisów,
  - hermetyzację: komunikacja z innymi modułami tylko na podstawie dobrze określonego i stabilnego kontraktu,
  - podatność na eksperymenty: możliwość ułatwienia sprawdzania innych rozwiązań i wykonania jakiegoś pivotu biznesowego czy technicznego,

- ... tylko niezależności wdrożeniowej nie posiada --- wciąż będzie podatny na wdrożenia jako wielkie święto i duże ryzyko.
