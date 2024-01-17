"""
Wersja 3.1


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
from flask import flash
from datetime import datetime

class Magazyn:
    def __init__(self):
        self.saldo = 0
        self.inventory = {}
        self.history = []
        self.plik_saldo = "magazyn_saldo.txt"
        self.plik_historia = "magazyn_history.txt"
        self.plik_magazyn = "magazyn_inventory.txt"
        self.wczytywanie = True

        self.load_data()

    def separator(self):
        print("_" * 40)

    def load_data(self):
        self.load_balance()
        self.load_history()
        self.load_inventory()

    def save_data(self):
        self.save_balance()
        self.save_history()
        self. save_inventory()

    def load_balance(self):
        try:
            with open(self.plik_saldo) as file:
                zawartosc = file.read().strip()
            if zawartosc:
                self.saldo = float(zawartosc)
            else:
                self.wczytywanie = False
                self.separator()
                print(f"Błąd: Plik \"{self.plik_saldo}\" jest pusty lub nie zawiera prawidłowej liczby.")
        except FileNotFoundError:
            self.wczytywanie = False
            self.separator()
            print(f"Błąd: Plik \"{self.plik_saldo}\" nie istnieje.")

    def load_history(self):
        try:
            with open(self.plik_historia, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    self.history = [line.strip() for line in lines]
                else:
                    self.wczytywanie = False
                    self.separator()
                    print(f"Błąd: Plik \"{self.plik_historia}\" jest pusty.")
        except FileNotFoundError:
            self.wczytywanie = False
            self.separator()
            print(f"Błąd: Plik \"{self.plik_historia}\" nie istnieje.")

    def load_inventory(self):
        try:
            with open(self.plik_magazyn, "r", encoding="utf-8") as file:
                lines = file.readlines()
            if not lines:
                self.wczytywanie = False
                self.separator()
                print(f"Plik \"{self.plik_magazyn}\" jest pusty.")
            else:
                for line in lines:
                    elements = line.strip().split(':', 1)
                    if len(elements) == 2:
                        key, value_str = elements
                        try:
                            value = eval(value_str)
                            self.inventory[key] = value
                        except (ValueError, SyntaxError) as e:
                            self.wczytywanie = False
                            self.separator()
                            print(f"Błąd: dot.: pliku: \"{self.plik_magazyn}\"")
                            print(f"Nie można przetworzyć wartości w linii:")
                            print(f"{line.strip()}")
                            print(f"Szczegóły: {e}")
                    else:
                        self.wczytywanie = False
                        self.separator()
                        print(f"Błąd: dot.: pliku: \"{self.plik_magazyn}\"")
                        print(f"Nieprawidłowy format linii: {line.strip()}")
        except FileNotFoundError:
            self.wczytywanie = False
            self.separator()
            print(f"Błąd: Plik \"{self.plik_magazyn}\" nie istnieje.")
        except Exception as e:
            self.wczytywanie = False
            self.separator()
            print(f"Dot.: dot.: pliku: \"{self.plik_magazyn}\"")
            print(f"Niespodziewany błąd: {e}")

        if self.wczytywanie:
            self.separator()
            print("Pliki wczytano pomyślnie.")
            self.separator()

    def save_balance(self):
        with open(self.plik_saldo, 'w') as file:
            file.write(str(self.saldo))

    def save_history(self):
        with open(self.plik_historia, "w", encoding="utf-8") as file:
            for item in self.history:
                file.write(item + '\n')

    def save_inventory(self):
        with open(self.plik_magazyn, "w", encoding="utf-8") as file:
            for key, value in self.inventory.items():
                file.write(f"{key}:{value}\n")

    def add_operation(self, operation):
        # Pobierz bieżącą datę i godzinę
        aktualna_data_i_godzina = datetime.now()
        # Sformatuj datę i godzinę jako string
        formatted_data_i_godzina = aktualna_data_i_godzina.strftime("%Y-%m-%d %H:%M:%S")
        operation =  formatted_data_i_godzina + ": " +  operation
        self.history.append(operation)

    def display_operations(self, start_index, end_index):
        for i in range(start_index, end_index + 1):
            if 0 <= i < len(self.history):
                print(f"Operacja {i + 1}: {self.history[i]}")
            else:
                print(f"Indeks {i + 1} poza zakresem historii.")


    def module_saldo(self):
        print("Moduł saldo")
        while True:
            try:
                input_kwota = input("Podaj kwotę: ")
                kwota = float(input_kwota)
                self.saldo += kwota
                self.add_operation("Zmieniono saldo o kwotę:", f"{kwota:.2F} PLN.")
                break
            except ValueError:
                print("Błąd! Wprowadź prawidłową kwotę.")

    def module_sprzedaz(self, nazwa, ilosc_input):
        flash(f"Sprzedano: {nazwa}, {ilosc_input} szt.")  # Dodajemy wiadomość do wyświetlenia na ekranie
        if not nazwa in self.inventory:
           flash(f"Towar o nazwie '{nazwa}' nie istnieje w magazynie.")
        else:
            # ilosc_input = input("Podaj ilość sztuk: ")
            ilosc_sprzedaz = int(ilosc_input)
            if ilosc_sprzedaz > 0:
                stan_magazynowy = self.inventory[nazwa]['ilosc']
                if stan_magazynowy < ilosc_sprzedaz:
                    flash("Za mały stan magazynowy. Możesz sprzedać max.: {stan_magazynowy} szt.")
                else:
                    stan_magazynowy -= ilosc_sprzedaz
                    self.inventory[nazwa]['ilosc'] = stan_magazynowy
                    self.saldo += (ilosc_sprzedaz * self.inventory[nazwa]['cena'])
                    tekst = "Sprzedaż:", f"{nazwa}, cena: {self.inventory[nazwa]['cena']:.2f} PLN, ilość: {ilosc_sprzedaz}."
                    self.add_operation(tekst)
            else:
                flash("Podano ujemną ilość do sprzedaży.")

    def module_zakup(self):
        print("Moduł zakup")
        nazwa = input("Podaj nazwę towaru: ")
        if nazwa in self.inventory:
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
            elif cena * ilosc > self.saldo:
                print("*" * 35)
                print("Za mały stan konta. Dodaj środki.")
                print("Nie dodano do magazynu.")
                print("*" * 35)
            else:
                self.inventory[nazwa] = {'cena': cena, 'ilosc': ilosc}
                self.add_operation("Zakup:", f"{nazwa}, cena: {cena:.2f} PLN, ilość: {ilosc}.")
                self.saldo = self.saldo - (cena * ilosc)
                print(f"Nowy towar '{nazwa}' został dodany do magazynu.")

    def module_konto(self):
        tekst = "{:,.2f}".format(self.saldo).replace(",", " ").replace(".", ",")
        return tekst

    def module_lista(self):
        print("Aktualny stan magazynu:")
        for nazwa, dane in self.inventory.items():
            print(f"Nazwa: {nazwa}, Cena: {dane['cena']:.2f} PLN, Ilość: {dane['ilosc']}")
        return self.inventory

    def module_przeglad(self):
        print("Moduł przegląd")
        return self.history
