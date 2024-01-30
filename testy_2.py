from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker

# Utwórz silnik SQLAlchemy, który będzie łączył się z bazą danych
engine = create_engine('sqlite:///accountant.db')

# Utwórz sesję SQLAlchemy, która będzie zarządzała połączeniem z bazą danych
Session = sessionmaker(bind=engine)
session = Session()

# Załaduj definicje tabel z bazy danych
metadata = MetaData()
inventory = Table('inventory', metadata, autoload_with=engine)
history = Table('history', metadata, autoload_with=engine)
saldo = Table('saldo', metadata, autoload_with=engine)

# Otwórz plik i przeczytaj dane
with open('magazyn_inventory.txt', 'r') as f:
    for line in f:
        product, rest = line.split(":", 1)
        items = rest.replace("{", "").replace("}", "").split(",")
        price = float(items[0].split(":")[1].strip())
        price_sql = price * 100
        quantity = int(items[1].split(":")[1].strip())

        # Wstaw dane do tabeli
        session.execute(inventory.insert().values(product=product, price=price_sql, quantity=quantity))

# Zatwierdź zmiany i zamknij sesję
session.commit()
session.close()
