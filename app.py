"""
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
"""

import atexit
from flask import Flask, render_template, request, flash, redirect
from magazyn import Magazyn

app = Flask(__name__)

app.config["SECRET_KEY"] = "Tajny klucz"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa


uzytkownicy = {}
rejestr = []

magazyn = Magazyn()
magazyn.load_data()
"""
     Metody klasy Magazyn:
             == "1":
                self.module_saldo()
             == "2":
                self.module_sprzedaz()
             == "3":
                self.module_zakup()
             == "4":
                self.module_konto()
             == "5":
                self.module_lista()
             == "6":
                self.module_magazyn()
             == "7":
                self.module_przeglad()
             == "9":
                self.save_balance()
                self.save_history()
                self.save_inventory()
             == "0":
                self.save_balance()
                self.save_history()
                self.save_inventory()
"""


@app.route('/')
def index():
     return render_template('index.html', konto=magazyn.module_konto(), stany=magazyn.inventory)


@app.route('/zakup', methods=["GET", "POST"])
def zakup():
    if request.form:
        nazwa = request.form.get("productNameBuy")
        if nazwa in magazyn.inventory:
            flash(f"Towar o nazwie '{nazwa}' już istnieje w magazynie.")
        cena_input = request.form.get("unitPriceBuy")
        cena = float(cena_input)
        if cena < 0:
            flash("Uwaga: cena zakupu mniejsza od 0.")
        else:
            ilosc_input = request.form.get("quantityBuy")
            ilosc = int(ilosc_input)
            if ilosc < 0:
                flash("Podano ilość mniejszą od 0.")
            elif cena * ilosc > magazyn.saldo:
                flash("Za mały stan konta. Dodaj środki.")
                flash("Nie dodano do magazynu.")
                flash("*" * 35)
            else:
                if nazwa in magazyn.inventory:
                    ilosc += magazyn.inventory[nazwa]['ilosc']
                else:
                    magazyn.saldo = magazyn.saldo - (cena * ilosc)
                    magazyn.inventory[nazwa] = {'cena': f"{cena:.2f}", 'ilosc': ilosc}
                tekst = f"Zakup: {nazwa}, cena: {cena:.2f} PLN, ilość: {ilosc}."
                magazyn.add_operation(tekst)

                magazyn.save_data()
                flash(f"Nowy towar '{nazwa}' został dodany do magazynu.")
    return render_template('zakup.html', konto=magazyn.module_konto())


@app.route('/sprzedaz', methods = ["GET", "POST"])
def sprzedaz():
    if request.form:
        productNameSell = request.form.get("productNameSell")
        quantitySell = request.form.get("quantitySell")
        if not productNameSell in magazyn.inventory:
            flash(f"Towar o nazwie '{productNameSell}' nie istnieje w magazynie.")
        else:
            ilosc_sprzedaz = int(quantitySell)
            if ilosc_sprzedaz > 0:
                stan_magazynowy = magazyn.inventory[productNameSell]['ilosc']
                if stan_magazynowy < ilosc_sprzedaz:
                    flash(f"Za mały stan magazynowy. Możesz sprzedać max.: {stan_magazynowy} szt.")
                else:
                    stan_magazynowy -= ilosc_sprzedaz
                    magazyn.inventory[productNameSell]['ilosc'] = stan_magazynowy
                    magazyn.saldo += (ilosc_sprzedaz * magazyn.inventory[productNameSell]['cena'])
                    tekst = f"Sprzedaż: {productNameSell}, ilość: {ilosc_sprzedaz} szt."
                    magazyn.add_operation(tekst)
                    magazyn.save_data()
                    flash(f"Sprzedano: {productNameSell}, {quantitySell} szt.")
            else:
                flash("Podano ujemną ilość do sprzedaży.")
        # return redirect("/")  # Przekierowuje do konkretnego widoku wykonując kod z przypisanej funkcji
    return render_template('sprzedaz.html', magazyn=magazyn.inventory)


@app.route('/saldo', methods = ["GET", "POST"])
def saldo():
    if request.form:
        while True:
            try:
                input_kwota = request.form.get("value")
                kwota = float(input_kwota)
                magazyn.saldo += kwota
                tekst = f"Zmieniono saldo o kwotę: {kwota:.2F} PLN"
                magazyn.add_operation(tekst)
                magazyn.save_data()
                break
            except ValueError:
                flash("Błąd! Wprowadź prawidłową kwotę.")
    return render_template('saldo.html',
                           konto=magazyn.module_konto())

@app.route('/historia')
def historia():
    return render_template('historia.html', history=magazyn.module_przeglad())

@app.route('/historia/<int:historia_from>/<int:historia_to>')
def historia_from_to(historia_from, historia_to):
    historia_to_show = []
    if len(magazyn.history) == 0:
        flash("Brak operacji w historii.")
    elif historia_from > 0:
        od = historia_from - 1
        do = historia_to
        # Sprawdzanie i obsługa pustych wartości
        if not od:
            od = 0
        else:
            od = int(od)
        if not do:
            do = len(magazyn.history)
        else:
            do = int(do)
        # Sprawdzanie zakresu
        if od < 0 or do > len(magazyn.history) or od > do:
            flash(f"Błędny zakres. Dostępne indeksy od 1 do {len(magazyn.history)}")
            flash("Użyj notacji: /historia/<start>/<koniec>")
        else:
            # Wyświetlanie akcji w wybranym zakresie
            for i in range(od, do):
                if 0 <= i < len(magazyn.history):
                    historia_to_show.append(magazyn.history[i])
                else:
                    print(f"Indeks {i + 1} poza zakresem historii.")
    return render_template('historia.html',
                           history=historia_to_show)

@app.route('/about')
def about():
    return render_template('about.html')

def zapisanie_danych_do_plikow():
    magazyn.save_data()


# atexit.register(zapisanie_danych_do_plikow)
