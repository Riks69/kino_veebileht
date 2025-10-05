import sqlite3

# Ühendus andmebaasiga (tekitab faili kui seda pole)
conn = sqlite3.connect("movies.db")
c = conn.cursor()

# Loome tabeli
c.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    image TEXT
)
""")

# Lisame mõned näidisfilmid
movies = [
    ("Oppenheimer", "Elulooline draama tuumapommi isast.", "https://via.placeholder.com/150"),
    ("Barbie", "Fantaasiarikas komöödia plastimaailmas.", "https://via.placeholder.com/150"),
    ("Tenet", "Ajaga manipuleeriv ulmefilm.", "https://via.placeholder.com/150")
]

# Sisestame filmid tabelisse
c.executemany("INSERT INTO movies (title, description, image) VALUES (?, ?, ?)", movies)

# Salvestame ja sulgeme
conn.commit()
conn.close()

print("Andmebaas loodud ja filmid lisatud!")
