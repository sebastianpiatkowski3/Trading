import sqlite3

# Połącz się z bazą danych (lub utwórz ją, jeśli nie istnieje)
conn = sqlite3.connect('accountant.db')

# Utwórz kursor
c = conn.cursor()

# Utwórz tabelę
c.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        price INTEGER,
        quantity INTEGER,
        date_product data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
with open('magazyn_inventory.txt', 'r') as f:
    for line in f:
        # Podział linii na nazwę produktu i resztę
        product , rest = line.split(":" , 1)
        # Usunięcie nawiasów klamrowych i podział na poszczególne elementy
        items = rest.replace("{" , "").replace("}" , "").split(",")
        # Przypisanie wartości do zmiennych
        price = float(items[0].split(":")[1].strip())
        price_sql = price *100
        quantity = int(items[1].split(":")[1].strip())
        # Wpisz dane do tabeli
        c.execute("INSERT INTO inventory (product, price, quantity) VALUES (?, ?, ?)", (product, price_sql, quantity))

c.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        opis TEXT,
        date_product data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
with open('magazyn_history.txt', 'r') as f:
    for line in f:
        line = f.readlines()
for linia in line:
    c.execute("INSERT INTO history (opis) VALUES (?)" , (linia.strip() ,))

c.execute('''
    CREATE TABLE IF NOT EXISTS saldo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        saldo integer,
        date_product data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
with open('magazyn_saldo.txt', 'r') as f:
    for line in f:
        saldo = (line.strip().split())
        saldo = float(saldo[0])
        saldo_sql = int(saldo * 100)
        # Wpisz dane do tabeli
        c.execute("INSERT INTO saldo (saldo) VALUES (?)", (saldo_sql,))

# Zatwierdź zmiany i zamknij połączenie
conn.commit()
conn.close()
