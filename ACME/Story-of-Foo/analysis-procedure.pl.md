### Analiza domenowa

- [Procedura analizy domenowej z użyciem Event Storming](#procedura-analizy-domenowej-z-użyciem-event-storming)
  - [Motywacja](#motywacja)
  - [Procedura](#procedura)
    - [1. Jakie pojęcia w systemie przekładają się na produkty?](#1-jakie-pojęcia-w-systemie-przekładają-się-na-produkty)
    - [2. Na jakie pytania odpowiada system w odniesieniu do tych produktów?](#2-na-jakie-pytania-odpowiada-system-w-odniesieniu-do-tych-produktów)
    - [3. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań?](#3-jakie-zdarzenia-wpływają-na-zmianę-odpowiedzi-na-każde-z-tych-pytań)
    - [4. Jakie są relacje między tymi zdarzeniami?](#4-jakie-są-relacje-między-tymi-zdarzeniami)
    - [5. Wyłanianie kandydatów na poddomeny](#5-wyłanianie-kandydatów-na-poddomeny)
    - [6. Czy potencjalne poddomeny są istotnie różne?](#6-czy-potencjalne-poddomeny-są-istotnie-różne)
    - [7. Wyłanianie kandydatów na konteksty](#7-wyłanianie-kandydatów-na-konteksty)
    - [8. Czy któreś konteksty da się zredukować przez usunięcie niepotrzebnych szczegółów?](#8-czy-któreś-konteksty-da-się-zredukować-przez-usunięcie-niepotrzebnych-szczegółów)
    - [9. Czy dany kontekst zawiera w sobie wszystkie natychmiastowo potrzebne informacje?](#9-czy-dany-kontekst-zawiera-w-sobie-wszystkie-natychmiastowo-potrzebne-informacje)
    - [10. Czy każde pytanie domenowe ma kontekst, który jest dla niego pojedynczym źródłem prawdy?](#10-czy-każde-pytanie-domenowe-ma-kontekst-który-jest-dla-niego-pojedynczym-źródłem-prawdy)
    - [11. Czy dany kontekst nie próbuje posiadać danych lub odpowiedzialności, które nie są konieczne do odpowiedzi na postawione mu pytanie?](#11-czy-dany-kontekst-nie-próbuje-posiadać-danych-lub-odpowiedzialności-które-nie-są-konieczne-do-odpowiedzi-na-postawione-mu-pytanie)
    - [12. Które poddomeny są strategiczne?](#12-które-poddomeny-są-strategiczne)
    - [13. Wyłanianie kandydatów na moduły](#13-wyłanianie-kandydatów-na-moduły)
    - [14. Czy któreś konteksty są źródłem podatności systemu na częste zmiany?](#14-czy-któreś-konteksty-są-źródłem-podatności-systemu-na-częste-zmiany)
    - [15. Wyłanianie kandydatów na mikroserwisy](#15-wyłanianie-kandydatów-na-mikroserwisy)

# Procedura analizy domenowej z użyciem Event Storming

## Motywacja

- Zmiany, które przekraczają granice mikroserwisów są drogie i skomplikowane. Częste takie zmiany niweczą pierwotny cel architektury mikroserwisów: autonomiczność w działaniu i rozwoju.

- Celem tej procedury jest znalezienie takiego podziału rozwiązania technicznego, który optymalizowałby jego postać ze względu na potencjalne zmiany. Jest korzystne, aby inicjatywy do zmian — zarówno od strony biznesu, jak i techniczne — zawierały się wewnątrz możliwie małej ilości komponentów. W idealnym świecie chcielibyśmy, aby zmiany zamknęły się w jednym mikroserwisie.

- Podstawowym sposobem na osiągnięcie autonomii jest podzielenie monolitu na możliwie małe i niezależnie wdrażane komponenty. Zbyt duże mikroserwisy, wymuszają interakcję między zespołami i są przyczyną braku autonomii.

- Rozproszenie komponentów w architekturze mikroserwisów powoduje nieusuwalne koszty na komunikacji, mierzone w czasie wykonania i zużytego transferu, oraz konieczność uwzględnienia niedostępności w każdym z komponentów ([fallacies of distributed computing](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)). Wyzwania technologiczne, wynikające z infrastruktury koniecznej do uruchomienia mikroserwisów, zwielokrotniają koszt przygotowania samego rozwiązania biznesowego. Zbyt małe mikroserwisy powodują zbyt duży narzut na komunikację.

- Założenie, że można stworzyć wartościową architekturę IT, niezależnie od specyfiki domeny biznesowej, jest pułapką. W przypadku architektury mikroserwisowej jest to szczególnie prawdziwe: osadzenie jakiejś poddomeny biznesowej na mikroserwisach o nieskorelowanych granicach sprawi, że trzeba będzie te granice często przekraczać. Wytyczenie złych granic mikroserwisów przekłada się wprost na nieefektywną architekturę systemu.

- Wszystkie te czynniki sprawiają, że wyznaczanie granic mikroserwisów powinno mieć charakter decyzji świadomej procesów oraz kosztu w utrzymaniu.

- Zaproponowana tu metoda opiera się na założeniu, że wiedza jest dobrze skumulowana w organizacji, ale niekoniecznie równomiernie rozdystrybuowana. Ktoś wie jakie procesy system ma obsługiwać, ktoś inny zna kroki danego procesu. Z kolei deweloperzy i administratorzy wiedzą o ograniczeniach technicznych przygotowywanego rozwiązania.

- Procedura ma na celu takie przeszukanie domeny problemu, żeby wyselekcjonować kandydatów na poddomeny, najbliższych wartości biznesowej. W drugiej części procedury tworzony jest podział rozwiązania zgodnie z granicami wyznaczonych wcześniej poddomen: na konteksty, moduły i mikroserwisy.

## Procedura

### 1. Jakie pojęcia w systemie przekładają się na produkty?

- Spośród wszystkich pojęć, jakimi system operuje, za punkt wyjścia weźmy te, które nadają wartość systemowi.

- Chcemy mieć jak najprostsze rozumienie tych pojęć:
  - Produkt to coś, przynoszące klientowi jakąś korzyść, nadające się na cel istnienia systemu. Produkt oczywiście nie musi być materialny, może być usługą IT lub organizacyjną. Przelew w systemie elektronicznym czy prawo do obsługi okienkowej też nadaje się na produkt, jeśli spodziewamy się, że klient może chcieć za nie zapłacić.

  - System to rozwiązanie, mierzące się z jakimś problemem. System może być rozwiązaniem technicznym: oprogramowaniem lub usługą IT. Może też być rozwiązaniem organizacyjnym: zespołem lub procesem w organizacji. System będzie najwyższym piętrem abstrakcji rozwiązania ([C4 Model](https://c4model.com/)).

### 2. Na jakie pytania odpowiada system w odniesieniu do tych produktów?

- Metodą może być pójście za tropem problemów rozwiązywanych przez system i tego, które rozwiązania są źródłem wartości systemu dla klienta.

- Wszystkich potencjalnych pytań jest zbyt dużo, żeby rozważanie wszystkich dało efektywne planowanie. Spośród nich, warto wybierać te, które wyciągają podstawowy sens istnienia systemu.

### 3. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań?

- Po co?
  - Skoro system ma dostarczać jakaś wartość, to prawdopodobnie wykonuje jakąś zmianę z korzyścią dla klienta. Chcemy wyłapać ciąg zdarzeń, który prowadzi do osiągnięcia tej zmiany.
  - Na tym etapie, poszukujemy kluczowych zdarzeń, obsługiwanych przez system wobec produktu, a przez to procesów, które system musi obsłużyć.

- Co jest zdarzeniem?
  - Zdarzenia są tu w rozumieniu zdarzenia domenowego:
    - zmiany zachowania danego pojęcia („*zamówienie zostało zablokowane*”),
    - zmiany stanu procesu biznesowego („*zamówienie przeszło do realizacji*”),
    - przemianę pojęcia w inne pojęcie („*konspekt został zamieniony w zamówienie*”).

  - Nie są zdarzeniami domenowymi:
    - kliknięcie przycisku „*Dalej*” w interfejsie,
    - zmiana jakiejś wartości w bazie,
    - reakcja interfejsu na zmienione dane.

- Które zdarzenia są dobre?
  - Zaczynamy od typowych „dobrych kandydatów”:
    - zdarzenie, które jest celem procesu („*Pieniądze trafiły na konto docelowe*”),
    - zdarzenie, będące kluczowym krokiem lub największym wyzwaniem do osiągnięcia celu („*Wniosek kredytowy został zaakceptowany*”).

  - Złymi kandydatami są te, które odwołują się do struktury wewnętrznej pojęć („*zmieniono numer konta docelowego*” albo „*wybrano urząd skarbowy*”). Taki sposób wyrażania może zasłaniać brak związku z domeną, skupienie na nieistotnych szczegółach lub utożsamienie różnych znaczeń:
    - struktura reprezentacji pojęć zmienia się często,
    - pojęcia, użyte jako podmioty opisu zdarzeń, mogą ukrywać wieloznaczne zachowanie („produkt” albo „zamówienie” ma zupełnie inne zachowania dla domeny fakturowania niż dla domeny marketingowej).

- Dobrym narzędziem do poszukiwań odpowiedzi na to pytanie jest [Event](https://www.eventstorming.com/) [Storming](https://radekmaziarka.pl/2018/12/06/event-storming-jak-szybko-odkrywac-nieznane/) ([ES](https://www.youtube.com/watch?v=u4aFjePJJTM)). To technika warsztatowa, która koordynuje wymianę wiedzy i szukanie wiarygodnych kandydatów na poddomeny w możliwie skondensowany i empiryczny sposób, pomijając niepotrzebne na danym etapie szczegóły.

- Czy zdarzenie powinno się pojawić?
  - Potencjalnych zdarzeń jest zbyt dużo, dlatego skupiamy się na tych, które mają znaczenie dla pytań z punktu 2. Jeśli zdarzenie nie odwzorowuje się na jakieś pytanie, to albo należy zweryfikować czy nie pominęliśmy jakiegoś pytania/produktu, albo zdarzenie jest w tym momencie nieistotne.

- A jeśli zdarzenia są zbyt mało wymowne?
  - Zacznij od wymodelowania jednego skonkretyzowanego procesu. Konkretny typ użytkownika w konkretnej sytuacji chce osiągnąć konkretny cel za konkretną kwotę.
  - Następnie szukaj alternatywnych początków i rozwidleń procesu.
  - Szukaj znaczenia ukrytego za mechanicznymi czynnościami. Naciśnięcie „*Dalej*” zazwyczaj oznacza coś ważnego dla domeny.
  - Bądź sceptyczny wobec nazw typu CRUD. Prawdopodobnie „*zaktualizowano*” znaczy coś bardziej konkretnego dla domeny.

### 4. Jakie są relacje między tymi zdarzeniami?

- Jak poukładać zdarzenia na osi czasu?
- Jak szukać kolejnych istotnych zdarzeń? Szukamy przez określenie źródła lub celu zdarzeń już znalezionych. Pomagają w tym pytania o relacje, np.:

  - Dlaczego?
  - Czy może zdarzyć się inaczej?
  - Kiedy się stało?
  - Jakie rzeczy muszą się zdarzyć wcześniej?
  - Kto to zmienia?
  - Czy można to powtórzyć?
  - Czy można to wycofać?
  - Jak często się zmienia?

- Pytania na podstawie analizy *Being, Behaving, Becoming* ([*Rethinking Systems Analysis and Design*](https://leanpub.com/rethinkingsystemsanalysisanddesign), G. Weinberg)

- Większość zdarzeń układa się w mniej lub bardziej regularne grupy, gdzie zachodzą:
  - następstwo w czasie albo skutkach,
  - uwspólnianie zdarzeń między różnymi procesami,
  - alternatywne ścieżki procesu,
  - alternatywne wejścia do procesu,
  - etc.

- Przerwy między zdarzeniami w czasie lub przestrzeni (w systemie lub organizacji) mogą sugerować [...].

### 5. Wyłanianie kandydatów na poddomeny

- Grupy zdarzeń domenowych stają się naturalnymi kandydatami na poddomeny. Obecność grup może wskazywać na potrzebę jakiejś spójności (np. danych lub czasu), natomiast przerwy w procesie są naturalnymi kandydatami do rozdzielenia.

- Kolejną możliwością wyłaniania poddomen jest zakres kompetencji konkretnego analityka bądź zespołu, pracującego w tej domenie. Ponieważ inicjatywa do formułowania zmiany w systemie jest oddawana w czyjeś ręce, dookoła kompetencji i pojęć tej osoby/zespołu będzie kształtowała się zmiana w systemie.

- Struktura organizacyjna może być źródłem wiedzy o poddomenach, ale równie dobrze może oddawać nieaktualny albo nieoptymalny podział organizacji na silosy. Typowym nieoptymalnym podziałem są silosy ze względu na kompetencje z procesu zatrudnienia pracownika: programiści kontra admini kontra analitycy systemowi kontra analitycy biznesowi.

### 6. Czy potencjalne poddomeny są istotnie różne?

- Z listy wymagań, zbioru User Story czy zestawu makiet ekranów w sposób automatyczny nie wynika wiedza o domenie.
- Analiza nie jest jednak tylko powierzchowną obserwacją zdarzeń:

  - > Trzeba sobie tu jasno powiedzieć, że indukcyjne podejście do analizy (zbieranie i zapisywanie obserwacji w celu identyfikacji trendu lub powtórzeń) przypomina próby zrozumienia gry w szachy metodą wielokrotnej obserwacji rozgrywek. Im wierniejszy opis gry ma powstać, tym więcej obserwacji należy udokumentować, co nie zmienia faktu, że taki dokument nie mówi absolutnie nic o przyszłych rozgrywkach. Alternatywą jest dedukcyjne podejście, polegające na zrozumieniu i opracowaniu, możliwie najmniejszym nakładem pracy, reguł gry w szachy, czego udokumentowanie wymaga najwyżej dwóch stron papieru A4, taki dokument opisuje także w 100% wszystkie przyszłe rozgrywki…
      >
      > — J. Żeliński, [Biznesowy model danych — nie chcemy.](https://it-consulting.pl/autoinstalator/wordpress/2017/02/03/biznesowy-model-danych-nie-chcemy/)
- Czy można usunąć jakąś ilość szczegółów z opisu poddomen, utrzymując taki sam opis procesu mniejszą ilością zdarzeń?

### 7. Wyłanianie kandydatów na konteksty

- Tu kończy się przeszukiwanie przestrzeni problemu, a zaczyna szukanie modelu rozwiązania.
- Domyślnie, każda z poddomen staje się tzw. bounded contextem (dalej: konteksty). Kontekst jest „bounded”, bo związany jest modelem (opisem pojęciami, którym nadajemy ścisłe znaczenie) z poddomeną, w której te znaczenia mają konkretny sens.
- Posiadanie kontekstów jeden do jednego może jednak być przesadnie dokładne i przez to niekorzystne, dlatego w dalszych krokach szukamy uproszczeń.

### 8. Czy któreś konteksty da się zredukować przez usunięcie niepotrzebnych szczegółów?

- Czy opis poddomeny zawiera elementy nieodwzorowane na jej zdarzeniach domenowych?
- Uogólnienie przez usunięcie nieistotnych szczegółów może doprowadzić do prostszego systemu i uwspólnienia kontekstów różnych poddomen.

### 9. Czy dany kontekst zawiera w sobie wszystkie natychmiastowo potrzebne informacje?

- Potrzebne informacje to te konieczne do odpowiedzi na całe pytanie i obsługi wszystkich zdarzeń jego poddomeny?
- Jeśli brakuje krytycznego kawałka informacji, może trzeba zespolić go z innym kontekstem.

### 10. Czy każde pytanie domenowe ma kontekst, który jest dla niego pojedynczym źródłem prawdy?

- Hipotetyczna sytuacja, w której trzeba odpytać 10 mikroserwisów, żeby dowiedzieć się, że dana funkcja jest wykonalna, jest z wielu powodów niekorzystna:
  - Gdy dziesiąta odpowiedź wróci, to pierwsza może być już nieaktualna.
  - Można to rozwiązywać jakimś wzorcem koordynacji: 2-phase-commit, saga.
  - Niezależnie od wybranego wzorca, rozproszona transakcja zwielokrotnia już i tak dużą liczbę komunikatów między serwisami.
  - Wzrost ilości komunikacji synchronicznej oznacza większą podatność na błędy połączeń.
- Zasada [Single Source of Truth]() w wersji dla architektury mikroserwisowej:
  - Jest dokładnie jeden mikroserwis odpowiadający na dane pytanie poddomeny. Reszta mikroserwisów może mieć cache'a tej informacji, jeśli akceptuje *eventual consistency*.
  - Każda żądanie zmiany odpowiedzi na to pytanie powinno być skierowane do tego mikroserwisu.

### 11. Czy dany kontekst nie próbuje posiadać danych lub odpowiedzialności, które nie są konieczne do odpowiedzi na postawione mu pytanie?

- Dwa poprzednie pytania prowadziły gromadzeniem informacji w bardziej bogate konteksty. Niniejsza zasada adresuje problem niepotrzebnie nagromadzonych odpowiedzialności.
- Tzw. *Data/Feature Envy* jest szybką drogą do zgubienia niezależności między kandydatami na mikroserwisy.

### 12. Które poddomeny są strategiczne?

- Czy jakaś poddomena jest specyfiką biznesową systemu? Odpowiada za kluczowe cechy produktu i jest źródłem jego przewagi rynkowej?
- Czy może oczekiwania wobec tej poddomeny są jeszcze niezbyt dobrze sformułowane?
- A może przyciąga małą ilość klientów i daje niewielki zysk?
- Poddomeny strategiczne w szczególności mogą potrzebować własnego kontekstu, bo tam jest duża szansa na pojawianie się inicjatyw do zmian i potrzebę szybkiej adaptacji.
- Pozostałe poddomeny mogą dostawać ze strony organizacji mniejszą uwagę albo być na tyle typowe czy rzadko zmienne, że będzie akceptowalne, że są realizowane przez systemy legacy albo „na piechotę”.

### 13. Wyłanianie kandydatów na moduły

- Tu zaczyna się implementacja.
- Strategiczne konteksty stają się naturalnym kandydatem do realizacji jako moduły (w rozumieniu architektury aplikacyjnej).
- Moduł to implementacja o szczegółach implementacyjnych odseparowanych od otaczającego go kodu, z ustalonym i upublicznionym kontraktem komunikacji.
- Moduł może mieć postać:
  - oddzielnego repozytorium,
  - wydzielonego pakietu w ramach wspólnego repozytorium,
  - oddzielnego podkatalogu w ramach wspólnego pakietu.
- Im większa izolacja, tym silniejsze zabezpieczenie przed niezamierzonymi ingerencjami. Ostatecznie, zdolny i zmotywowany deweloper naruszy dowolny poziom izolacji.
- Podobnie jak z kontekstami, zbyt drobny lub zbyt gruby podział na moduły wymusi nadmiarową zależność lub komunikację.
- *Coupling & Cohesion*.

### 14. Czy któreś konteksty są źródłem podatności systemu na częste zmiany?

- Czy jakiś kontekst jest chaotyczny, trudne do zanalizowania?
- Czy jakiś kontekst ma specjalne potrzeby techniczne, np. bardzo wysoką dostępność?
- A może potrzebujemy oddać taki kontekst jakiemuś konkretnemu zespołowi ze względu na podział pracy albo trudność w znalezieniu developerów?
- Takie szczególne cechy kontekstu wskazują na potrzebę umieszczenia go w wyodrębnionym module, aby nie zaburzać rytmu rozwoju pozostałych modułów.
- Za wydzieleniem do osobnego modułu mogą iść szczególne standardy implementacyjne, na przykład *linting*, wymagania na testy jednostkowe, standardy recenzji itd.

### 15. Wyłanianie kandydatów na mikroserwisy

- Dopiero na tym etapie decydujemy o architekturze wdrożeniowej.

- Modułom o dobrze określonych granicach ich kontekstu nadajemy charakter mikroserwisu na przykład, wtedy gdy:

  - chcemy zapewnić niezależność wdrożeniową,
  - mają często zmienną logikę biznesową,
  - mają wymaganie wysokiej high availability,
  - w szczególny sposób muszą mieć dostrojony model wdrożeniowy ze względu na normy ISO czy polityki bezpieczeństwa.

- Czasem świadomie możemy nie chcieć wydzielać mikroserwisów z modułów na przykład, wtedy gdy:

  - nie jesteśmy jeszcze pewni granic kontekstu dookoła takiego modułu,
  - gdy jest to związane z niedekomponowalnym systemem legacy, od którego kontekst zależy,
  - zmienia się rzadko i jest peryferyjny dla domeny.

- Ostatecznie, zdekomponowany na moduły, ale nie wdrożony w mikroserwisy monolit też zapewnia część cech popularnie oczekiwanych od mikroserwisów:

  - *skalowalność*: moduły też można zwielokrotnić całością monolitu i włączać/wyłączać feature-flagami; kosztem jest *jedynie* pamięć operacyjna,
  - *niezależność rozwoju*: monolit nie musi koniecznie pochodzić z mono-repozytorium, może dawać zespołom niezależność developmentu, choć nie zabezpieczoną fizycznymi granicami maszyny, na której to jest uruchomione, jak w przypadku mikroserwisów,
  - *hermetyzację*: komunikacja z innymi modułami tylko na podstawie dobrze określonego i stabilnego kontraktu,
  - *podatność na eksperymenty*: ułatwienie sprawdzania innych rozwiązań i wykonania jakiegoś pivotu biznesowego czy technicznego,

- Ostatecznym powodem dla posiadania mikroserwisów jest potrzeba zmniejszenia ryzyk ze względu na wdrożenie.
- Aby minimalizować ryzyko, należy zapewnić niezależność tak infrastrukturalną, jak i implementacyjną i domenową.
