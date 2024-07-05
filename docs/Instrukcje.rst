Instrukcja
==========
Instrukcje podane niżej dotyczą działania funkcji z poziomu programu. Dodatkowo pozwalają też zrozumieć działanie aplikacji z perspektywy użytkownika.

Dodatkowa informacja dot. Aplikacji
"""""""""""""""""""""""""""""""""""

Aplikacja składa sie z dwóch trybów
- standardowego
- trybu bazy danych (database mode)

W pierwszym mamy dostęp do funkcji umożliwiających dodanie odpowiednich wpisów. W drugim natomiast zyskujemy dostęp do funkcji zaawansowanych takich jak:
- modyfikacja danych 
- usuwanie danych 
- wykonywanie i wyświetlanie zapytań
- oraz sortowanie tabel

Wszystkie funkcje są opsługiwane przez dialog z użytkownikiem, który wybiera odpowiednie czynności lub podaje odpowiednie dane w odpowiedzi. Wszystkie dane wprowadzane są wcześniej sprawdzane pod kątem zgodności.


DBHandling
----------

**Funkcje wporowadzające dane do lokalnej bazy danych oraz te pozwalające zarządzanie nią.**

.. automodule:: Aplikacja.DBHandling
   :members:
   :undoc-members:
   :show-inheritance:
   
postgress
---------

**Funkcje wporowadzające dane do zdalnej bazy danych. Umożliwiaja także budowę zadanych danych.**

.. automodule:: Backend.postgress 
   :members:
   :undoc-members:
   :show-inheritance:

