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

from flask import Flask, render_template, request, flash, redirect, g
from sqlalchemy import func , ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from magazyn import Magazyn
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app_info = {
    'db_file' : r'C:\Users\sebas\SQLite3\accountant.db'
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accountant.db'
app.config["SECRET_KEY"] = "Tajny klucz"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa

uzytkownicy = {}
rejestr = []
magazyn = Magazyn()

db = SQLAlchemy(app)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db. Column(db.Integer)

    # Relacja z tabelą History
    historia = relationship('History' , back_populates = 'inventory')

"""
Ustanawiam powiązanie między tabelami History a Inventory w SQLAlchemy.
W tym celu dodaję kolumnę inventory_id do tabeli History jako klucz obcy,
a następnie ustanawiam odpowiednie relacje.
Dodano kolumnę inventory_id do tabeli History jako klucz obcy odnoszący się do kolumny id w tabeli Inventory.
W tabeli Inventory dodano relację historia, a w tabeli History dodano relację inventory.
back_populates informuje SQLAlchemy o wzajemnym powiązaniu tych relacji.
"""

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String)
    when = db.Column(db.DateTime, server_default=func.now())

    # Dodanie klucza obcego
    inventory_id = db.Column(db.Integer , ForeignKey('inventory.id'))
    # Ustanowienie relacji do tabeli Inventory
    inventory = relationship('Inventory' , back_populates = 'historia')

    # Klucz obcy do tabeli EventType
    event_type_id = db.Column(db.Integer , ForeignKey('event_type.id'))
    # Relacja do tabeli EventType
    event_type = relationship('EventType')

class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float)
    when = db.Column(db.DateTime, server_default=func.now())

"""
Tworzę dodatkową tabelę z definicjami zdarzeń, żeby przechowywać jedynie identyfikator zdarzenia w tabeli History.
To jest podejście znane jako normalizacja danych, co może być dobrym pomysłem w sytuacjach,
gdzie chcę uniknąć powtarzania tych samych informacji w różnych miejscach,
co może prowadzić do redundancji i trudności w utrzymaniu spójności danych.
To podejście pozwala na bardziej elastyczne zarządzanie rodzajami zdarzeń,
a także ułatwia utrzymanie spójności danych,
ponieważ definicje zdarzeń są przechowywane tylko w jednym miejscu.
"""
class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String, unique=True)  # np. 'Zakup', 'Sprzedaz', 'Zmiana Salda'
    history_entries = relationship('History' , back_populates = 'event_type')


# Przykładowe dane
sample_data = [
    {'product': 'Laptop', 'price': 1500, 'quantity': 10},
    {'product': 'Monitor', 'price': 300, 'quantity': 20},
    {'product': 'Keyboard', 'price': 50, 'quantity': 30},
    {'product': 'Mouse', 'price': 20, 'quantity': 40},
    {'product': 'Printer', 'price': 200, 'quantity': 15},
    {'product': 'External Hard Drive', 'price': 100, 'quantity': 25},
    {'product': 'SSD', 'price': 80, 'quantity': 35},
    {'product': 'Graphics Card', 'price': 400, 'quantity': 10},
    {'product': 'RAM', 'price': 60, 'quantity': 30},
    {'product': 'Processor', 'price': 300, 'quantity': 15},
    {'product': 'Motherboard', 'price': 150, 'quantity': 20},
    {'product': 'Router', 'price': 80, 'quantity': 25},
    {'product': 'Webcam', 'price': 30, 'quantity': 40},
    {'product': 'Headphones', 'price': 50, 'quantity': 30},
    {'product': 'Microphone', 'price': 40, 'quantity': 25},
    {'product': 'USB Flash Drive', 'price': 10, 'quantity': 50},
    {'product': 'Software License', 'price': 100, 'quantity': 15},
    {'product': 'Server', 'price': 1000, 'quantity': 5},
    {'product': 'UPS', 'price': 150, 'quantity': 10},
    {'product': 'Desk Chair', 'price': 120, 'quantity': 8},
]



with app.app_context():
    db.create_all()
    db.session.commit()

    # # Dodanie definicji zdarzenia (jeśli jeszcze nie istnieje)
    # zdarzenie_zakup = EventType(event_type = 'Zakup')
    # db.session.add(zdarzenie_zakup)
    # db.session.commit()
    # zdarzenie_sprzedaz = EventType(event_type = 'Sprzedaz')
    # db.session.add(zdarzenie_sprzedaz)
    # db.session.commit()
    # zdarzenie_saldo = EventType(event_type = 'Zmiana_Salda')
    # db.session.add(zdarzenie_saldo)
    # db.session.commit()


    # # Dodawanie przykładowych danych do bazy
    # for data in sample_data:
    #     inventory_entry = Inventory(**data)
    #     db.session.add(inventory_entry)
    #     # Commit zmian
    #     db.session.commit()

    # Dodaj dane do tabeli Inventory
    # for data in sample_data:
    #     product = Inventory(product = data['product'] , price = data['price'] ,
    #                         quantity = data['quantity'])
    #     db.session.add(product)
    #     db.session.commit()
    #
    # # Pobierz przykładowe dane z tabeli EventType
    # event_type_purchase = EventType.query.filter_by(
    #     event_type = 'Zakup').first()
    # event_type_sale = EventType.query.filter_by(event_type = 'Sale').first()
    # event_type_balance_change = EventType.query.filter_by(
    #     event_type = 'Balance_Change').first()
    #
    # # Dodaj przykładowe zdarzenia do tabeli History
    # for data in sample_data:
    #     # Załóżmy, że każde zdarzenie to zakup (możesz dostosować to według potrzeb)
    #     event_text = f"Zakup: {data['product']}, cena: {data['price']}, ilość: {data['quantity']}"
    #     event = History(event=event_text, when=datetime.now(), inventory=product, event_type=event_type_purchase)
    #     db.session.add(event)
    #     db.session.commit()

        # Załóżmy, że istnieją także sprzedaże i zmiany salda (możesz dostosować to według potrzeb)
        # Dodaj odpowiednie zdarzenia i dostosuj event_type
        # ...

def zapisz_saldo(kwota, tekst):
    saldo_sql = Saldo.query.order_by(Saldo.id.desc()).first()

    if saldo_sql is None:
        saldo_sql = Saldo(saldo = kwota)
    else:
        saldo_sql = Saldo(saldo = saldo_sql.saldo + kwota)

    # Dodaj nowy rekord do sesji SQLAlchemy
    db.session.add(saldo_sql)
    db.session.commit()

    # Tworzenie nowego rekordu w tabeli History z powiązanym zakupem
    event_type_zakup = EventType.query.filter_by(event_type = 'Zmiana_Salda').first()
    history = History(event = tekst , event_type = event_type_zakup ,
                      inventory = '')
    db.session.add(history)
    db.session.commit()

@app.route('/')
def index():
    magazyn_stan = Inventory.query.all()
    #magazyn_stan = Inventory.query.order_by(Inventory.product).all()  #  Sort this by product name
    magazyn_stan = sorted(Inventory.query.all() , key = lambda x: x.product.lower())

    # get the last saldo from table Saldo
    konto = Saldo.query.order_by(Saldo.id.desc()).first()
    if konto is None:
        konto = 0
    else:
        konto = konto.saldo
    return render_template('index.html', konto=konto, magazyn=magazyn_stan)


@app.route('/zakup', methods=["GET", "POST"])
def zakup():
    if request.form:
        konto = Saldo.query.order_by(Saldo.id.desc()).first()
        magazyn_saldo = konto.saldo
        nazwa = request.form.get("productNameBuy")
        cena_input = request.form.get("unitPriceBuy")
        cena = float(cena_input)
        if cena < 0:
            flash("Uwaga: cena zakupu mniejsza od 0.")
        else:
            ilosc_input = request.form.get("quantityBuy")
            ilosc = int(ilosc_input)
            if ilosc < 0:
                flash("Podano ilość mniejszą od 0.")
            elif cena * ilosc > magazyn_saldo:
                flash("Za mały stan konta. Dodaj środki.")
                flash("Nie dodano do magazynu.")
                flash("*" * 35)
            else:
                #   Check if product name already exists in database (in table Inventory in column product
                if Inventory.query.filter_by(product = nazwa).first():
                    flash(f"Towar o nazwie '{nazwa}' już istnieje w magazynie.")
                    #  Change quantity in Inventory table for existing product to quantity+=ilosc
                    produkt = Inventory.query.filter_by(product = nazwa).first()
                    produkt.quantity += ilosc
                    db.session.commit()
                    """
                    Wygląda na to, że w Twoim kodzie występuje błąd. Komunikat o błędzie wskazuje, że próbujesz uzyskać dostęp do atrybutu o nazwie `_sa_instance_state` na obiekcie typu `str`, co nie jest możliwe. Ten błąd często występuje podczas korzystania z SQLAlchemy w Pythonie.

Na podstawie Twojego kodu wydaje się, że problem dotyczy funkcji `zakup` w Twojej aplikacji Flask. Funkcja próbuje utworzyć nowy obiekt `History` z atrybutami `event`, `event_type_zakup` i `inventory`, ale atrybut `inventory` jest obiektem typu `str`, a nie instancją klasy `Inventory`.

Aby naprawić ten błąd, upewnij się, że atrybut `inventory` jest instancją klasy `Inventory` przed przekazaniem go do konstruktora `History`. Możesz również sprawdzić, czy atrybuty `event` i `event_type_zakup` są poprawnie ustawione.

    produkt = Inventory.query.filter_by(product=nazwa).first()
    history = History(event=tekst, event_type=event_type_zakup, inventory=produkt)
W powyższym kodzie `produkt` jest obiektem typu `Inventory`, który jest przekazywany do konstruktora `History` jako atrybut `inventory`.    

...a było:
    nazwa = request.form.get("productNameBuy")
    history = History(event=tekst, event_type=event_type_zakup, inventory=nazwa)
    
Powyższy kod pobiera pierwszy rekord z tabeli `Inventory`, który ma wartość `product` równą `nazwa`. Następnie aktualizuje wartość atrybutu `quantity` o wartość `ilosc`. Na końcu tworzy nowy obiekt `History` z atrybutami `event`, `event_type_zakup` i `inventory` i zapisuje go w bazie danych za pomocą metody `commit()`.
"""
                    event_type_zakup = EventType.query.filter_by(
                        event_type = 'Zakup').first()
                    tekst = f"Zakup istniejącego w bazie towaru: {nazwa}, cena: {produkt.price:.2f} PLN, ilość: {ilosc}."
                    history = History(event = tekst ,
                                      event_type = event_type_zakup ,
                                      inventory = produkt)
                    db.session.add(history)
                    db.session.commit()

                else:
                    """
                    Kiedy tworzę nowy rekord w tabeli History po dokonaniu zakupu,
                    przypisuję konkretny rekord z tabeli Inventory do kolumny inventory:
                    """
                    # Tworzenie nowego rekordu w tabeli Inventory
                    new_product = Inventory(product=nazwa, price=cena, quantity=ilosc)
                    db.session.add(new_product)
                    db.session.commit()

                    # Sprawdź, czy istnieje rekord w tabeli EventType o nazwie 'Zakup'
                    """
                    EventType.query.filter_by(event_type='Zakup').first()
                    służy do pobrania rekordu z tabeli EventType, który ma określony rodzaj zdarzenia ('Zakup').
                    Pozwala to na uzyskanie obiektu EventType z bazy danych,
                    który można wykorzystać do powiązania z obiektem History w celu utworzenia nowego wpisu w tabeli historii.
                    W rezultacie, event_type_zakup będzie zawierać obiekt EventType,
                    który ma rodzaj zdarzenia ustawiony na 'Zakup'.
                    Jeśli nie istnieje taki rekord, event_type_zakup będzie równy None.
                    """
                    event_type_zakup = EventType.query.filter_by(event_type = 'Zakup').first()
                    tekst = f"Zakup: {nazwa}, cena: {cena:.2f} PLN, ilość: {ilosc}."  # string do zapisu w historii
                    # Tworzenie nowego rekordu w tabeli History z powiązanym zakupem
                    history = History(event=tekst, event_type=event_type_zakup, inventory=new_product)
                    db.session.add(history)
                    db.session.commit()

                    magazyn_saldo = magazyn_saldo - (cena * ilosc)
                    # zapisz_saldo(magazyn_saldo, tekst)  # Zapisanie salda do bazy danych

                    flash(f"Nowy towar '{nazwa}' został dodany do magazynu.")

    # get the last saldo from table Saldo
    konto = Saldo.query.order_by(Saldo.id.desc()).first()
    if konto is None:
        konto = 0
    else:
        konto = konto.saldo

    return render_template('zakup.html', konto=konto)


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
                    magazyn.saldo -= (ilosc_sprzedaz * float(magazyn.inventory[productNameSell]['cena']))

                    # Znajdź produkt w magazynie
                    produkt = Inventory.query.filter_by(product = productNameSell).first()

                    if produkt:
                        # Aktualizuj stan magazynowy (zmniejsz ilość)
                        produkt.quantity -= ilosc_sprzedaz
                        db.session.commit()

                    # Sprawdź, czy istnieje rekord w tabeli EventType o nazwie 'Zakup'
                    event_type = EventType.query.filter_by(event_type = 'Sale').first()
                    tekst = f"Sprzedaż: {productNameSell}, ilość: {ilosc_sprzedaz} szt."
                    # Tworzenie nowego rekordu w tabeli History z powiązanym zakupem
                    history = History(event=tekst, event_type=event_type, inventory=produkt)
                    db.session.add(history)
                    db.session.commit()

                    magazyn.add_operation(tekst)
                    magazyn.save_data()
                    flash(f"Sprzedano: {productNameSell}, {quantitySell} szt.")
            else:
                flash("Podano ujemną ilość do sprzedaży.")
        # return redirect("/")  # Przekierowuje do konkretnego widoku wykonując kod z przypisanej funkcji
    magazyn_stan = Inventory.query.all()
    # get the last saldo from table Saldo
    konto = Saldo.query.order_by(Saldo.id.desc()).first()
    if konto is None:
        konto = 0
    else:
        konto = konto.saldo
    return render_template('sprzedaz.html', magazyn_sql=magazyn_stan, magazyn=magazyn.inventory)


@app.route('/saldo', methods = ["GET", "POST"])
def saldo():
    if request.form:
        while True:
            try:
                input_kwota = request.form.get("value")
                kwota = float(input_kwota)

                # Pobierz ostatnie saldo z tabeli Saldo
                #  do not Shadow name 'saldo' from outer scope

                saldo_sql = Saldo.query.order_by(Saldo.id.desc()).first()

                if saldo_sql is None:
                    saldo_sql = Saldo(saldo = kwota)
                else:
                    saldo_sql = Saldo(saldo = saldo_sql.saldo + kwota)

                # Dodaj nowy rekord do sesji SQLAlchemy
                db.session.add(saldo_sql)
                db.session.commit()


                tekst = f"Zmieniono saldo o kwotę: {kwota:.2F} PLN"

                break
            except ValueError:
                flash("Błąd! Wprowadź prawidłową kwotę.")
    # get the last saldo from table Saldo
    konto = Saldo.query.order_by(Saldo.id.desc()).first()
    if konto is None:
        konto = 0
    else:
        konto = konto.saldo
    return render_template('saldo.html', konto=konto)

@app.route('/historia')
def historia():
    przeglad_historia = History.query.all()
    return render_template('historia.html', history=przeglad_historia)

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
    historia_sql = History.query.all()
    # get the last saldo from table Saldo
    konto = Saldo.query.order_by(Saldo.id.desc()).first()
    if konto is None:
        konto = 0
    else:
        konto = konto.saldo
    return render_template('historia.html', historia_sql=historia_sql,
                           history=historia_to_show)

@app.route('/about')
def about():
    return render_template('about.html')

def zapisanie_danych_do_plikow():
    magazyn.save_data()


# atexit.register(zapisanie_danych_do_plikow)

if __name__ == '__main__':
    app.run(debug=True)


def config():
    return None