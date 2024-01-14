"""

Wersja 2.1 dodano obsługę błędów podczas wczytywania plików z:
- wielkoscią salda
- historią operacji
- stanem magazynowym
_______________________________________________________________________________

Na podstawie zadania z lekcji 5 (operacje na koncie, sprzedaż/zakup itp.)
należy zaimplementować poniższą część:

Saldo konta oraz magazyn mają zostać zapisane do pliku tekstowego,
 a przy kolejnym uruchomieniu programu ma zostać odczytany.
Zapisać należy również historię operacji (przegląd),
 która powinna być rozszerzana przy każdym kolejnym uruchomieniu programu.

"""
dostepne_komendy = """
Dostępne komendy:
1 - Saldo
2 - Sprzedaż
3 - Zakup
4 - Konto
5 - Lista
6 - Magazyn
7 - Przegląd
9 - Zapisz
0 - Koniec
"""

saldo = 0 # Globalna zmienna ze stanem konta
inventory = {}  # Globalna zmienna do przechowywania stanu magazynu
history = []  # Lista do przechowywania historii operacji
plik_saldo = "magazyn_saldo.txt"  # Plik z saldem magazynu
plik_historia = "magazyn_history.txt"  # Plik z historią operacji
plik_magazyn = "magazyn_inventory.txt"  # Plik ze stanem magazynu
wczytywanie = True  # Zmienna przechowuje wynik poprawnego wczytywania plików

def separator():
    print("_" * 40)

def add_operation(operation, var1): # Funkcja wpisująca operacje do historii
    history.append(operation + " " + var1)

def display_operations(start_index, end_index): # Funkcja do printowania operacji z zakresu
    for i in range(start_index, end_index + 1):
        if 0 <= i < len(history):
            print(f"Operacja {i + 1}: {history[i]}")
        else:
            print(f"Indeks {i + 1} poza zakresem historii.")

def save_saldo():
    # Otwórz plik do zapisu
    with open('magazyn_saldo.txt', 'w') as file:
        # Zapisz zmienną do pliku
        file.write(str(saldo))

def save_history(): # Funkcja zapisująca historię do pliku
    with open("magazyn_history.txt", "w", encoding="utf-8") as file:
        for item in history:
            file.write(item + '\n')


def save_inventory(): # Funkcja zapisująca stan magazynu do pliku
    with open("magazyn_inventory.txt", "w", encoding="utf-8") as file:
        for key, value in inventory.items():
            file.write(f"{key}:{value}\n")


print("_" * 40)
print("Aplikacja do zarządzania magazynem")
print ("Moduł: Python 9: Import lokalny, pliki tekstowe")
print("Autor: Sebastian Piątkowski")

with open(plik_saldo) as zawartosc_pliku:
    zawartosc = zawartosc_pliku.read().strip()  # Usunięcie ewentualnych białych znaków na początku i końcu
if zawartosc:
    saldo = float(zawartosc)
else:
    wczytywanie = False
    separator()
    print(f"Błąd: Plik \"{plik_saldo}\" jest pusty lub nie zawiera prawidłowej liczby.")

with open(plik_historia, "r", encoding="utf-8") as file:
    lines = file.readlines()
    if lines:
        history = [line.strip() for line in lines]
    else:
        wczytywanie = False
        separator()
        print(f"Błąd: Plik \"{plik_historia}\" jest pusty.")

"""
Otwiera plik ze stanem magazynu. Obsługuje błędy takie jak:
- pusty plik
- błędny format linii
  (sprawdzenie liczby elementów w linii przed jej przetworzeniem)
- ewentualne błędy podczas ewaluacji wartości
  (użycie bloku try-except do obsługi błędów konwersji)
"""

try:
    with open(plik_magazyn, "r", encoding="utf-8") as file:
        lines = file.readlines()
    if not lines:
        wczytywanie = False
        separator()
        print(f"Plik \"{plik_magazyn}\" jest pusty.")
    else:
        for line in lines:
            elements = line.strip().split(':', 1)
            if len(elements) == 2:
                key, value_str = elements
                try:
                    value = eval(value_str)
                    inventory[key] = value
                except (ValueError, SyntaxError) as e:
                    wczytywanie = False
                    separator()
                    print(f"Błąd: dot.: pliku: \"{plik_magazyn}\"")
                    print(f"Nie można przetworzyć wartości w linii:")
                    print(f"{line.strip()}")
                    print(f"Szczegóły: {e}")
            else:
                wczytywanie = False
                separator()
                print(f"Błąd: dot.: pliku: \"{plik_magazyn}\"")
                print(f"Nieprawidłowy format linii: {line.strip()}")
except FileNotFoundError:
    wczytywanie = False
    separator()
    print(f"Błąd: Plik \"{plik_magazyn}\" nie istnieje.")
except Exception as e:
    wczytywanie = False
    separator()
    print(f"Dot.: dot.: pliku: \"{plik_magazyn}\"")
    print(f"Niespodziewany błąd: {e}")
if wczytywanie:
    separator()
    print("Pliki wczytano pomyślnie.")
separator()
# ^Koniec wczytywania plików_________________________________________________________________________

while True:
    print(dostepne_komendy)
    komenda = input("Podaj numer komendy: ")

    if komenda == "1":
        print("Moduł saldo")
        while True:
            try:
                input_kwota = input("Podaj kwotę: ")
                kwota = float(input_kwota)
                saldo += kwota
                add_operation("Zmieniono saldo o kwotę:", f"{kwota:.2F} PLN.")
                break
            except ValueError:
                print("Błąd! Wprowadź prawidłową kwotę.")
    elif komenda == "2":
        print("Moduł sprzedaż")
        nazwa = (input("Podaj nazwę towaru: "))
        # Sprawdź, czy towar już istnieje w magazynie
        if not nazwa in inventory:
            print(f"Towar o nazwie '{nazwa}' nie istnieje w magazynie.")
        else:
            ilosc_input = input("Podaj ilość sztuk: ")
            ilosc_sprzedaz = int(ilosc_input)
            if ilosc_sprzedaz > 0:
                # Sprawdź, czy jest wystarczająca ilość w magazynie.
                stan_magazynowy = inventory[nazwa]['ilosc']
                if stan_magazynowy < ilosc_sprzedaz:
                    print("*" * 35)
                    print("Za mały stan magazynowy.")
                    print(f"Możesz sprzedać max.: {stan_magazynowy} szt.")
                    print("*" * 35)
                else:
                    # Zdejmij sprzedany towar z magazynu
                    stan_magazynowy -= ilosc_sprzedaz
                    inventory[nazwa]['ilosc'] = stan_magazynowy
                    saldo += (ilosc_sprzedaz * inventory[nazwa]['cena'])
                    add_operation("Sprzedaż:", f"{nazwa}, cena: {inventory[nazwa]['cena']:.2f} PLN, ilość: {ilosc_sprzedaz}.")
            else:
                print("Podano ujemną ilość do sprzedaży.")
    elif komenda == "3":
        print("Moduł zakup") # Historia
        nazwa = (input("Podaj nazwę towaru: "))
        # Sprawdź, czy towar już istnieje w magazynie
        if nazwa in inventory:
            print(f"Towar o nazwie '{nazwa}' już istnieje w magazynie.")
        cena_input = input("Podaj cenę towaru: ")
        cena = float(cena_input)
        if cena < 0:
            print("Uwaga: cena zakupu mniejsza od 0.")
        else:
            ilosc_input = input("Podaj ilość sztuk: ")
            ilosc = int(ilosc_input)
            if ilosc < 0:
                print("Podano ilość mniejszą od 0.")
            # Sprawdź, czy są wystarczające środki na koncie.
            elif cena * ilosc > saldo:
                print("*" * 35)
                print("Za mały stan konta. Dodaj środki.")
                print("Nie dodano do magazynu.")
                print("*" * 35)
            else:
                # Dodaj nowy towar do magazynu
                inventory[nazwa] = {'cena': cena, 'ilosc': ilosc}
                add_operation("Zakup:", f"{nazwa}, cena: {cena:.2f} PLN, ilość: {ilosc}.")
                saldo = saldo - (cena * ilosc)
                print(f"Nowy towar '{nazwa}' został dodany do magazynu.")
    elif komenda == "4": # Moduł wyświetla stan konta
        #print("Moduł konto")
        print (f"Stan konta: {saldo:.2f} PLN")
    elif komenda == "5":
        print("Moduł lista")
        print("Aktualny stan magazynu:")
        for nazwa, dane in inventory.items():
            print(f"Nazwa: {nazwa}, Cena: {dane['cena']:.2f} PLN, Ilość: {dane['ilosc']}")
    elif komenda == "6":
        print("Moduł magazyn")
        nazwa_produktu = input("Podaj nazwę produktu: ")
        if nazwa_produktu in inventory:
            print(f"Stan magazynu dla produktu '{nazwa_produktu}':")
            print(f"Cena: {inventory[nazwa_produktu]['cena']:.2f} PLN")
            print(f"Ilość: {inventory[nazwa_produktu]['ilosc']}")
        else:
             print(f"Produkt o nazwie '{nazwa_produktu}' nie istnieje w magazynie.")
    elif komenda == "7":
        print("Moduł przegląd")
        if len(history) == 0:
            print("Brak operacji w historii.")
        else:
            od = input("Podaj indeks początkowy (od): ")
            do = input("Podaj indeks końcowy (do): ")
            # Sprawdzanie i obsługa pustych wartości
            if not od:
                od = 0
            else:
                od = int(od)
            if not do:
                do = len(history)
            else:
                do = int(do)
            # Sprawdzanie zakresu
            if od < 0 or do > len(history) or od > do:
                print("Błędny zakres. Dostępne indeksy od 1 do", len(history))
                print("Liczba zapisanych komend:", len(history))
            else:
                # Wyświetlanie akcji w wybranym zakresie
                for i in range(od, do):
                    if 0 <= i < len(history):
                        print(f"Operacja {i + 1}: {history[i]}")
                    else:
                        print(f"Indeks {i + 1} poza zakresem historii.")

    elif komenda == "9":
        save_saldo()
        save_history()
        save_inventory()

    elif komenda == "0":
        save_saldo()
        save_history()
        save_inventory()
        print("Koniec działania programu")
        break
