'''
Projekty strony głównej i podstron dla systemu accountant

Zadanie polega na zaprojektowaniu strony głównej dla aplikacji do zarządzania magazynem i księgowością oraz podstrony "Historia".

1.Strona główna powinna zawierać następujące elementy:

Wyświetlanie aktualnego stanu magazynowego i aktualnego salda.
Trzy formularze:
a. Formularz do zakupu: z polami: nazwa produktu, cena jednostkowa, liczba sztuk.
b. Formularz do sprzedaży: z polami: nazwa produktu, cena jednostkowa, liczba sztuk.
c. Formularz zmiany salda: z polami: komentarz, wartość (tylko liczbowa).

2.Podstrona "Historia"

Podstrona powinna być dostępna pod adresem "/historia/" i "/historia/<line_from>/<line_to>/"
Jeśli nie podano parametrów, powinna wyświetlać całą historię.
Jeśli podano parametry, powinna wyświetlać dane z danego zakresu.

3.CSS

Zapewnij przyjazny dla użytkownika interfejs, stosując style CSS.
'''


from flask import Flask, render_template


app = Flask(__name__)


class WarehouseManagement():
    def __init__(self):
        self.dostepne_komendy = """
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
        self.saldo = 0
        self.inventory = {}
        self.history = []
        self.plik_saldo = "magazyn_saldo.txt"
        self.plik_historia = "magazyn_history.txt"
        self.plik_magazyn = "magazyn_inventory.txt"
        self.wczytywanie = True

    # saldo = 0 # Globalna zmienna ze stanem konta
    # inventory = {}  # Globalna zmienna do przechowywania stanu magazynu
    # history = []  # Lista do przechowywania historii operacji
    # plik_saldo = "magazyn_saldo.txt"  # Plik z saldem magazynu
    # plik_historia = "magazyn_history.txt"  # Plik z historią operacji
    # plik_magazyn = "magazyn_inventory.txt"  # Plik ze stanem magazynu
    # wczytywanie = True  # Zmienna przechowuje wynik poprawnego wczytywania plików


    def separator(self):
        print("_" * 40)


    def add_operation(self, operation, var1):
        self.history.append(operation + " " + var1)


    def display_operations(self, start_index, end_index):
        for i in range(start_index, end_index + 1):
            if 0 <= i < len(self.history):
                print(f"Operacja {i + 1}: {self.history[i]}")
            else:
                print(f"Indeks {i + 1} poza zakresem historii.")


    def save_saldo(self):
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


    def load_files(self):
        try:
            with open(self.plik_saldo) as zawartosc_pliku:
                zawartosc = zawartosc_pliku.read().strip()
            if zawartosc:
                self.saldo = float(zawartosc)
            else:
                self.wczytywanie = False
                self.separator()
                print(
                    f"Błąd: Plik \"{self.plik_saldo}\" jest pusty lub nie zawiera prawidłowej liczby.")

            with open(self.plik_historia, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    self.history = [line.strip() for line in lines]
                else:
                    self.wczytywanie = False
                    self.separator()
                    print(f"Błąd: Plik \"{self.plik_historia}\" jest pusty.")

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
        except FileNotFoundError:
            self.wczytywanie = False
            self.separator()
            print("Błąd: Brak jednego z plików do wczytania.")

#
# while True:
#     print(dostepne_komendy)
#     komenda = input("Podaj numer komendy: ")

    def saldo(self):
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


    def sprzedaz(self):
        print("Moduł sprzedaż")
        nazwa = (input("Podaj nazwę towaru: "))
        # Sprawdź, czy towar już istnieje w magazynie
        if not nazwa in self.inventory:
            print(f"Towar o nazwie '{nazwa}' nie istnieje w magazynie.")
        else:
            ilosc_input = input("Podaj ilość sztuk: ")
            ilosc_sprzedaz = int(ilosc_input)
            if ilosc_sprzedaz > 0:
                # Sprawdź, czy jest wystarczająca ilość w magazynie.
                stan_magazynowy = self.inventory[nazwa]['ilosc']
                if stan_magazynowy < ilosc_sprzedaz:
                    print("*" * 35)
                    print("Za mały stan magazynowy.")
                    print(f"Możesz sprzedać max.: {stan_magazynowy} szt.")
                    print("*" * 35)
                else:
                    # Zdejmij sprzedany towar z magazynu
                    stan_magazynowy -= ilosc_sprzedaz
                    self.inventory[nazwa]['ilosc'] = stan_magazynowy
                    self.saldo += (ilosc_sprzedaz * self.inventory[nazwa]['cena'])
                    self.add_operation("Sprzedaż:", f"{nazwa}, cena: {self.inventory[nazwa]['cena']:.2f} PLN, ilość: {ilosc_sprzedaz}.")
            else:
                print("Podano ujemną ilość do sprzedaży.")

    def zakup(self):
        print("Moduł zakup") # Historia
        nazwa = (input("Podaj nazwę towaru: "))
        # Sprawdź, czy towar już istnieje w magazynie
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
            # Sprawdź, czy są wystarczające środki na koncie.
            elif cena * ilosc > self.saldo:
                print("*" * 35)
                print("Za mały stan konta. Dodaj środki.")
                print("Nie dodano do magazynu.")
                print("*" * 35)
            else:
                # Dodaj nowy towar do magazynu
                self.inventory[nazwa] = {'cena': cena, 'ilosc': ilosc}
                self.add_operation("Zakup:", f"{nazwa}, cena: {cena:.2f} PLN, ilość: {ilosc}.")
                saldo = self.saldo - (cena * ilosc)
                print(f"Nowy towar '{nazwa}' został dodany do magazynu.")


    def konto(self): # Moduł wyświetla stan konta
        #print("Moduł konto")
        saldo = str(f'{self.saldo:.2f}')
        print(f"Stan konta: {saldo} PLN")
        return saldo

    def stan_magazynu(self):
        print("Moduł lista")
        print("Aktualny stan magazynu:")
        for nazwa, dane in self.inventory.items():
            print(f"Nazwa: {nazwa}, Cena: {dane['cena']:.2f} PLN, Ilość: {dane['ilosc']}")


    def magazyn(self):
        print("Moduł magazyn")
        nazwa_produktu = input("Podaj nazwę produktu: ")
        if nazwa_produktu in self.inventory:
            print(f"Stan magazynu dla produktu '{nazwa_produktu}':")
            print(f"Cena: {self.inventory[nazwa_produktu]['cena']:.2f} PLN")
            print(f"Ilość: {self.inventory[nazwa_produktu]['ilosc']}")
        else:
             print(f"Produkt o nazwie '{nazwa_produktu}' nie istnieje w magazynie.")


    def historia(self):
        print("Moduł przegląd")
        if len(self.history) == 0:
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
                do = len(self.history)
            else:
                do = int(do)
            # Sprawdzanie zakresu
            if od < 0 or do > len(self.history) or od > do:
                print("Błędny zakres. Dostępne indeksy od 1 do", len(self.history))
                print("Liczba zapisanych komend:", len(self.history))
            else:
                # Wyświetlanie akcji w wybranym zakresie
                for i in range(od, do):
                    if 0 <= i < len(self.history):
                        print(f"Operacja {i + 1}: {self.history[i]}")
                    else:
                        print(f"Indeks {i + 1} poza zakresem historii.")


    def zapisz_pliki(self):
        self.save_saldo()
        self.save_history()
        self.save_inventory()

    # elif komenda == "0":
    #     save_saldo()
    #     save_history()
    #     save_inventory()
    #     print("Koniec działania programu")


warehouse_management = WarehouseManagement()
warehouse_management.load_files()
warehouse_management.konto()

print(f'to jest flask')
print(warehouse_management.konto())
@app.route('/')
def index():
    return render_template('index2.html', saldo=warehouse_management.konto)

@app.route('/historia')
def historia():
    warehouse_management.konto()
    return render_template('historia.html')

@app.route('/linki')
def linki():
 body = '''<a href="http://www.google.com" target="_blank">Google</a> <br /> 
 <a href="http://www.bing.com" target="_blank">Default search engine to 
find Google</a>'''
 return body

@app.route("/druga")
def druga():
    return 'Druga podstrona (widok)'


@app.route('/trzecia')
def trzecia():
    return render_template('trzecia.html')


# @app.route('/template')
# def html_template():
#     return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)