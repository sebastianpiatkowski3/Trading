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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/historia')
def historia():
    return render_template('historia.html')



if __name__ == '__main__':
    app.run(debug=True)