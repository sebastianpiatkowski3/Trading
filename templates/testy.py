def formatuj_cene(cena_string):
    cena = float(cena_string)
    return "{:.2f}".format(cena)

print(formatuj_cene("1234"))     # Wydrukuje 1234.00
print(formatuj_cene("1234.12"))  # Wydrukuje 1234.12
