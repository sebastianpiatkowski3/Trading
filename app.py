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


from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from magazyn import Magazyn

app = Flask(__name__)

pp = Flask(__name__)
bootstrap = Bootstrap(app)

appHasRunBefore: bool = False  # w celu wykonania fragmentu kodu tylko raz w całym cyklu życia tego programu.

magazyn = Magazyn()
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
@app.before_request
def firstRun():
    global appHasRunBefore
    if not appHasRunBefore:
        appHasRunBefore = True
        print("Ten kod zostanie wykonany tylko raz w całym cyklu życia tego programu.")
        magazyn.load_data()


uzytkownicy = {
    'Anna': 'anna@example.com',
    'Kuba':'kjh@kjhk.pl',
    'Jan': 'jan@example.com',
    'Katarzyna': 'katarzyna@example.com',
    'Piotr': 'piotr@example.com',
    'Magdalena': 'magdalena@example.com',
    'Tomasz': 'tomasz@example.com',
    'Aleksandra': 'aleksandra@example.com',
    'Krzysztof': 'krzysztof@example.com',
    'Ewa': 'ewa@example.com',
    'Marcin': 'marcin@example.com'
}

@app.route('/', methods=["GET", "POST"])  # Dodajemy metodę POST aby wysłać formularz
def index():
    if request.form:  # Sprawdzamy, czy formularz przyszedł (zabezpieczenie przed brakiem formularza na metodzie GET)
        email = request.form.get("email")  # Wyciągamy pole "email" z formularza
        haslo = request.form.get("haslo")
        uzytkownicy[email] = haslo
    return render_template('index.html',
                           stany=magazyn.module_lista())


@app.route('/historia')
def historia():
    return render_template('historia.html',
                           history=magazyn.module_przeglad())



if __name__ == '__main__':
    app.run(debug=True)