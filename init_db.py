import sqlite3
from datetime import datetime, timedelta

def create_and_populate_db():
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()

    # Loo tabelid
    c.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        image TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS cinemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS halls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cinema_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS screenings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        hall_id INTEGER NOT NULL,
        start_time TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (hall_id) REFERENCES halls(id)
    )
    """)

    # Kustuta vana sisu, et vältida dubleerimist
    c.execute("DELETE FROM screenings")
    c.execute("DELETE FROM halls")
    c.execute("DELETE FROM cinemas")
    c.execute("DELETE FROM movies")

    # Lisa filmid
    movies = [
        ("Oppenheimer", "Elulooline draama tuumapommi isast.", "https://via.placeholder.com/150"),
        ("Barbie", "Fantaasiarikas komöödia plastimaailmas.", "https://via.placeholder.com/150"),
        ("Tenet", "Ajaga manipuleeriv ulmefilm.", "https://via.placeholder.com/150")
    ]
    c.executemany("INSERT INTO movies (title, description, image) VALUES (?, ?, ?)", movies)

    # Lisa kinod
    cinemas = [
        ("Apollo Solarise", "Tallinn, Solaris Kaubanduskeskus"),
        ("Coca-Cola Plaza", "Tallinn, Viru väljak 4")
    ]
    c.executemany("INSERT INTO cinemas (name, location) VALUES (?, ?)", cinemas)

    # Lisa saalid
    halls = [
        (1, "Saal 1"),
        (2, "Saal 3")
    ]
    c.executemany("INSERT INTO halls (cinema_id, name) VALUES (?, ?)", halls)

    # Lisa seansid (kasutades praegust aega)
    now = datetime.now()
    screenings = [
        (1, 1, (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), 9.50),
        (2, 2, (now + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"), 8.00),
        (3, 1, (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"), 7.50)
    ]
    c.executemany("INSERT INTO screenings (movie_id, hall_id, start_time, price) VALUES (?, ?, ?, ?)", screenings)

    conn.commit()
    conn.close()
    print("Andmebaas loodud ja täidetud näidisandmetega!")

if __name__ == "__main__":
    create_and_populate_db()
