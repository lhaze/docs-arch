### Analiza domenowa

# Wprowadzenie do prezentacji

- W ciągu jednego dnia, od trzech różnych osób, usłyszałem trzy sprzeczne między sobą zdania o naszej architekturze mikroserwisów:

  - „Serwis `bank-name` to nie jest mikroserwis, to nano-serwis. To powinno się znaleźć w serwisie `accounts`. Nie można tak drobiazgowo dzielić funkcji, żeby każdy komunikat znalazł się w osobnym serwisie”.
  - „`bank-name` nie nadaje się na serwis `accounts`, bo ten ostatni zajmuje się twoimi rachunkami, a nie obcymi. To inna domena. Co więcej, trzeba pokroić komunikaty. Jeśli komunikaty będą takie swiss-army-knife jak teraz, to nigdy nie będą mikroserwisami”.
  - „Nie ma perspektywy na cięcie komunikatów w ramach projektu chmurowania.”

- Próba uzasadnienia wariantu 2. doprowadziła mnie do próby opisania i zaspokojenia pewnej potrzeby: sformułowania powtarzalnej i empirycznej procedury dzielenia serwisu zgodnie z naturalnymi granicami jego domeny.

- Zastrzeżenie: podane tu fakty mają charakter orientacyjny. Mogą nie być prawdziwe i na pewno analiza nie jest wyczerpująca.

- Jeśli jakieś stwierdzenia lub wnioski są nieprawdziwe, poproszę o cierpliwość:
  - Treść analizy jest na podstawie ograniczonej wiedzy i ograniczonego czasu na przygotowanie.
  - Wersja właściwa powinna być wspólnym wkładem.
  - Jeśli nawet jakieś wnioski są oczywiste, to przedstawienie ich tutaj jako środek do prezentacji analizy domenowej.
  - Nie jestem AS, brakuje mi wiedzy, ale może też jest tak, że te pytania powinny po prostu zostać zadane.
