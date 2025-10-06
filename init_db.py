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

    # Add genres and movie_genres tables
    c.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS movie_genres (
        movie_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (genre_id) REFERENCES genres(id),
        PRIMARY KEY (movie_id, genre_id)
    )
    """)

    # Kustuta vana sisu, et vältida dubleerimist
    c.execute("DELETE FROM screenings")
    c.execute("DELETE FROM halls")
    c.execute("DELETE FROM cinemas")
    c.execute("DELETE FROM movie_genres")
    c.execute("DELETE FROM genres")
    c.execute("DELETE FROM movies")

    # Lisa filmid
    movies = [
        ("Oppenheimer", "Eluloofilm Ameerika teadlasest J. Robert Oppenheimerist ja aatomipommi loomisest. Võimas, sügav ja pingeline.", "https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg"),
        ("Barbie", "Elu Barbielandis on ideaalne… kuni Barbie avastab päris maailma. Teravmeelne ja visuaalselt kirev lugu eneseotsingutest.", "https://image.tmdb.org/t/p/original/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg"),
        ("Tenet", "Ajaga manipuleeriv ulmefilm.", "https://upload.wikimedia.org/wikipedia/en/1/14/Tenet_movie_poster.jpg"),
        ("The Holdovers", "Tundlik draama õpetajast ja õpilasest, kes veedavad koos jõulud internaatkoolis. Täis nostalgiat ja soojust.", "https://m.media-amazon.com/images/I/71eJickIHyL._AC_SL1500_.jpg"),
        ("Free Guy", "Videomängu kõrvaltegelasest saab ootamatult kangelane. Kiire tempo, palju nalja ja südamlik sõnum.", "https://upload.wikimedia.org/wikipedia/en/1/1c/Free_Guy_2021_Poster.jpg"),
        ("John Wick 4", "John Wick naaseb – rohkem lahinguid, rohkem adrenaliini. Filmis on efektne koreograafia ja pingeline tempo.", "https://m.media-amazon.com/images/I/81fk-N7tvbL._AC_SL1500_.jpg"), 
        ("Mission: Impossible – Dead Reckoning Part One", "Ethan Hunt seisab silmitsi oma senise ohtlikema missiooniga. Ülipõnev ja tehniliselt muljetavaldav märul.", "https://image.tmdb.org/t/p/original/bAZFkReuav0fyCVmWXBeUB93nAe.jpg"), 
        ("The Nun II", "Kurjus ründab taas. Järjefilm hirmutavast nuja selle ümber.", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWy_Qv11HRePQVTkGX9ctBV2nLXVo_xlpKOFMC4zlx1yLjhNbg"), 
        ("Talk to Me", "Noor seltskond leiab viisi surnutega suhtlemiseks… kuni asi läheb kontrolnnast, kes külvab hirmu kloostris li alt. Kaasaegne ja šokeeriv õudusfilm.", "https://image.tmdb.org/t/p/original/kdPMUMJzyYAc4roD52qavX0nLIC.jpg"), 
        ("Dune: Part Two", "Paul Atreides liitub fremenitega, et täide viia oma saatus. Epiline visuaal, poliitika ja müstika kõrvuti.", "https://upload.wikimedia.org/wikipedia/en/5/52/Dune_Part_Two_poster.jpeg"), 
        ("Everything Everywhere All At Once", "Tavaline naine satub multiversumisse, kus iga valik loob uue reaalsuse. Originaalne, pöörane ja sügavamõtteline.", "https://upload.wikimedia.org/wikipedia/en/1/1e/Everything_Everywhere_All_at_Once.jpg"), 
        ("Elemental", "Elementide linnas õpivad tuli ja vesi, et erinevused ei pea lahutama. Värvikas ja õpetlik animatsioon.", "https://m.media-amazon.com/images/I/718jC7PE5ZL._AC_SL1347_.jpg"), 
        ("Minions: The Rise of Gru", "Väikese Gru kurjategija karjääri algus. Palju nalja ja armastatud kollased tegelased.", "https://m.media-amazon.com/images/I/71pEZloYQHL._AC_SL1425_.jpg"), 
    ]
    c.executemany("INSERT INTO movies (title, description, image) VALUES (?, ?, ?)", movies)

    # Lisa kinod
    cinemas = [
        ("Apollo Solarise", "Tallinn, Solaris Kaubanduskeskus"),
        ("Coca-Cola Plaza", "Tallinn, Viru väljak 4"),
        ("Apollo Mustamäe", "Tallinn, Mustamäe Keskus"),
        ("Apollo Kristiine", "Tallinn, Kristiine Keskus"),
        ("Apollo Saaremaa", "Saaremaa, Auriga Keskus"),
        ("Apollo Viljandi", "Viljandi, Centrum Keskus"),
        ("Apollo Pärnu", "Pärnu, Pärnu Keskus"),
        ("Apollo Eeden", "Tartu, Eeden Kaubanduskeskus"),
        ("Apollo Lõunakeskus", "Tartu, Lõunakeskus"),
        ("Apollo Tasku", "Tartu, Tasku Keskus"),
        ("Apollo Jõhvi", "Jõhvi, Pargi Keskus"),
        ("Apollo Astri", "Narva, Astri Keskus"),
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

    # Lisa žanrid
    genres = [
        ("Action",),
        ("Drama",),
        ("Sci-Fi",),
        ("Comedy",),
        ("Animation",),
        ("Thriller",),
        ("Horror",),
        ("Biography",),
        ("Adventure",),
        ("Fantasy",)
    ]
    c.executemany("INSERT INTO genres (name) VALUES (?)", genres)

    # Seosed filmide ja žanride vahel
    movie_genres = [
        (1, 8),  # Oppenheimer - Biography
        (2, 4),  # Barbie - Comedy
        (3, 3),  # Tenet - Sci-Fi
        (4, 2),  # The Holdovers - Drama
        (5, 4),  # Free Guy - Comedy
        (6, 1),  # John Wick 4 - Action
        (7, 1),  # Mission Impossible - Action
        (8, 7),  # The Nun II - Horror
        (9, 7),  # Talk to Me - Horror
        (10, 9), # Dune: Part Two - Adventure
        (10, 3), # Dune: Part Two - Sci-Fi
        (11, 2), # Everything Everywhere All At Once - Drama
        (11, 3), # Everything Everywhere All At Once - Sci-Fi
        (12, 5), # Elemental - Animation
        (13, 5), # Minions - Animation
    ]
    c.executemany("INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)", movie_genres)

    conn.commit()
    conn.close()
    print("Andmebaas loodud ja täidetud näidisandmetega!")

if __name__ == "__main__":
    create_and_populate_db()