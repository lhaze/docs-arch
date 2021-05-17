### Analiza domenowa

- [Domena: Konta](#domena-konta)
  - [1. Jakie pojęcia w systemie przekładają się na produkty?](#1-jakie-pojęcia-w-systemie-przekładają-się-na-produkty)
  - [2. Na jakie pytania odpowiada system w odniesieniu do tych produktów?](#2-na-jakie-pytania-odpowiada-system-w-odniesieniu-do-tych-produktów)
    - [3. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań?](#3-jakie-zdarzenia-wpływają-na-zmianę-odpowiedzi-na-każde-z-tych-pytań)
    - [4. Jakie są relacje między tymi zdarzeniami?](#4-jakie-są-relacje-między-tymi-zdarzeniami)
    - [5. Wyłanianie kandydatów na poddomeny](#5-wyłanianie-kandydatów-na-poddomeny)
    - [6. Czy potencjalne poddomeny są istotnie różne?](#6-czy-potencjalne-poddomeny-są-istotnie-różne)

# Domena: Konta

- Zastrzeżenie: podane tu fakty mają charakter orientacyjny. Mogą nie być prawdziwe i na pewno analiza nie jest wyczerpująca.

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

- Czy posiadanie konta umożliwia mi dostęp do platformy bankowości elektronicznej?
  - Czy mam dostęp do systemu?
- Ile mam środków?
  - Jaka waluta?
- Czy w ogóle mogę wykonywać przelew?
  - Czy dostęp do systemu mam ograniczony?
- Czy z tego konta mogę wykonać przelew?
  - Czy mam wystarczająco dużo środków, żeby go wykonać?
  - Czy konto jest właściwego typu?
  - Czy jestem w odpowiedniej relacji do konta?
  - Czy mam odpowiedni poziom dostępu?
  - Czy zgadza się waluta?
- Komu chce przelać pieniądze?
  - Czy mam już dane odbiorcy przygotowane?
    - Czy mam zapisanego odbiorcę?
    - Czy mogę stworzyć przelew na podstawie operacji z historii konta?
  - Czy numer konta jest do właściwego odbiorcy?
    - Jaki bank obsługuje rachunek o tym numerze?
    - Jaki jest mój numer Indywidualnego Rachunku Podatkowego?
    - Jaki jest numer konta organu podatkowego dla danego formularza podatkowego?
- Ile mnie to będzie kosztować?
  - Jaki jest koszt typu przelewu?
  - Jaki sposób przewalutowania będzie użyty?
- Kiedy przelew dojdzie?
  - Jaki jest spodziewany termin dla typu przelewu?
  - Jaki ma wpływ kalendarz dni pracujących?
- Czy zaproponować ofertę produktu przy okazji przelewu?
  - Czy klient wyraził zgody marketingowe?
  - Czy klient ma już ten produkt?
  - Czy oferujemy klientowi produkt?
- Jak uzyskać bankowe potwierdzenie?
  - Przelewu
  - Salda
  - Właścicielstwa
- Czy mogę zamknąć konto?
- Skąd wziąć dokument zaświadczenia/wydruk?
  - Historia operacji
  - Potwierdzenie operacji

  -

### 3. Jakie zdarzenia wpływają na zmianę odpowiedzi na każde z tych pytań?

[diagram ES, krok 3]

### 4. Jakie są relacje między tymi zdarzeniami?

[diagram ES, krok 3a]

- Najbardziej znaczące relacje:
  - „*Zweryfikowano brak ograniczenia dostępu*” musi się zdarzyć przed każdym requestem.
  - „*Zautoryzowano operację*” pojawia się bardzo często i ma tę samą strukturę.
  - W grupie „*Zarejestrowano przelew*” operacje przeplata się z [...]

- W jakim stopniu istotne są szczegóły?
  - Między „*Zarejestrowano przelew*” a „*Zaprezentowano ofertę RTM*” dzieje się dużo szczegółów technicznych, włączając w to procesy w różnych systemach. Dla tego kroku nie mają znaczenia i, jeśli nie pojawią się w kolejnych krokach, to może w ogóle nie mają znaczenia dla podziału domenowego.
  
### 5. Wyłanianie kandydatów na poddomeny

Orientacyjna lista poddomen, na podstawie grup na planszy Event Stormingu. Na tym etapie wolno jej być zbyt drobiazgową lub nie do końca podzieloną.

1. Dostęp do systemu
2. Podpisanie umowy o konto
3. Weryfikacja tożsamości klienta
4. Historia i szczegóły operacji
5. Blokady na koncie
6. Właścicielstwo kont
7. Konta jako produkty z umową
8. Oferta produktów przy okazji obsługi konta
9. Zgody marketingowe
10. Limity związane z kontem
11. Saldo na koncie
12. Dyspozycja zamknięcie konta
13. Zaświadczenia o saldzie
14. Wydruk z wyciągiem
15. Zaświadczenie o posiadaczach
16. Wydruk ze szczegółami konta
17. Oszczędzanie w ramach konta/operacji
18. Dyspozycje i zapytania o egzekucje
19. Dyspozycje o przeniesieniu rachunku na innego właściciela
20. Dyspozycja przekazania wynagrodzenia
21. Dyspozycja na wypadek śmierci

- Oferta jest wyraźnie inną poddomeną, bo wiedza domenowa i inicjatywa do zmian skupiona jest w gronie innych analityków.
  - Poddomeną jest „Oferta”, a nie RTM czy CMS. Dla przykładu, CMS, jako kontener systemowy obsługuje tak samo proces RTM, jak i treści informacyjne z procesu logowania. To argument przeciwko podziałowi wynikającemu z kodu komponentów.

---

Domeny splątane ze sobą nie powinny być rozdzielnie analizowane:

- Konta i operacje na koncie (przelewy itd.) nie są rozdzielnymi domenami: w centrum procesów obu domen siedzi poddomena salda na koncie.
- Konta i karty nie są rozdzielnymi domenami: operacje z karty muszą być rozliczone w ramach jakiegoś konta.

Niektóre procesy w interfejsie wyglądają jakby były z tej samej poddomeny, ale różnią pojęciami i źródłem informacji:

- Historia operacji i blokady na koncie mogą znajdować się na jednym widoku, ale informacja, którą przedstawiają, pochodzi z różnych źródeł i co innego oznacza.

### 6. Czy potencjalne poddomeny są istotnie różne?

Pewne poddomeny można uwspólnić ze względu na dużą ilość wspólnych zdarzeń i ich wymagań:

- Przelewy walutowe dla różnych walut mają ten sam proces, różnice są w parametryzacji procesu. Zdarzenia, jakie składają się na ich procesy, są tożsame. Sytuacja na planszy Event Stormingu wykazuje to.
- Dyspozycje mogą mieć ten sam proces wnioskowania/obiegu dokumentu, więc z perspektywy systemu frontowego mogą być jedną poddomeną.
- Autoryzacja operacji nie różni się ze względu na operację, ale różni się ze względu na własne wewnętrzne dane i polityki, np. rodzaj narzędzia autoryzacyjnego.
  - Autoryzacja operacji ma własną poddomenę, wspólną dla wszystkich operacji na koncie, ale też np. dla zaprezentowania właścicieli. Tylko w ograniczonym stopniu związana z samą operacją.

---

- Autoryzacja operacji jako wydzielony bounded context:
  - (+) Współdzielenie procesu jako podprocesu przez różne poddomeny
  - (+) Konieczna wysoka dostępność
  - (+) Lekko opóźniona spójność

- Bounded contexty jako ratunek na problemy z backendem
  - Składanie wniosków: obecnie:
    - złożenie wniosku
    - wejście na listę wniosków
    - brak wpisu
    - przelogowanie
    - wciąż nic
    - czekamy
    - o, wniosek się pojawił
  - Składanie wniosków: propozycja
    - złożenie wniosku
    - własny obiekt domenowy zmienia stan na dodatkowy stan, reprezentujący optimistic consistency
    - weryfikacja stanu obiektu domenowego na podstawie obiektu backendowego
