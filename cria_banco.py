import sqlite3


connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

cria_tabela = 'CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, \
               nome text, estrelas real, diaria real, cidade texto)'

cria_hotel = "INSERT INTO hoteis VALUES ('Master', 'Mater Hotel', 3.8, 200, 'Mauá')"
               
cursor.execute(cria_tabela)
cursor.execute(cria_hotel)
connection.commit()
connection.close()