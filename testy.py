from datetime import datetime

# Pobierz bieżącą datę i godzinę
aktualna_data_i_godzina = datetime.now()

# Sformatuj datę i godzinę jako string
formatted_data_i_godzina = aktualna_data_i_godzina.strftime("%Y-%m-%d %H:%M:%S")

# Twórz string z bieżącą datą i godziną
tekst_z_data_i_godzina = f'Teraz jest: {formatted_data_i_godzina}'

# Wyświetl rezultat
print(tekst_z_data_i_godzina)
