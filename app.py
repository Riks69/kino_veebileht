from flask import Flask, render_template, g, abort, redirect, url_for, request, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'suvasaladussõna'  # Flash sõnumite jaoks

DATABASE = 'movies.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Võimaldab kasutada ridu nagu sõnastikke
    return db

def get_available_seats(screening_id):
    db = get_db()
    cur = db.cursor()

    # Leia ekraanikuva saal
    cur.execute("SELECT hall_id FROM screenings WHERE id = ?", (screening_id,))
    hall_row = cur.fetchone()
    if not hall_row:
        return []
    hall_id = hall_row["hall_id"]

    # Kõik istmed selles saalis
    cur.execute("SELECT id, seat_number FROM seats WHERE hall_id = ?", (hall_id,))
    seats = cur.fetchall()

    # Kõik juba müüdud istmed sellele seansile
    cur.execute("SELECT seat_id FROM tickets WHERE screening_id = ?", (screening_id,))
    taken_seats = {row["seat_id"] for row in cur.fetchall()}

    # Vabad istmed
    available = [seat for seat in seats if seat["id"] not in taken_seats]

    return available

def get_taken_seats(screening_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT seat_id FROM tickets WHERE screening_id = ?", (screening_id,))
    taken = {row["seat_id"] for row in cur.fetchall()}
    return taken

def buy_ticket_in_db(screening_id, seat_id):
    db = get_db()
    cur = db.cursor()

    # Kontrolli, kas istekoht on juba müüdud
    cur.execute("SELECT COUNT(*) FROM tickets WHERE screening_id = ? AND seat_id = ?", (screening_id, seat_id))
    if cur.fetchone()[0] > 0:
        return False

    purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Lisa pilet
    cur.execute("INSERT INTO tickets (screening_id, seat_id, purchase_time) VALUES (?, ?, ?)", (screening_id, seat_id, purchase_time))
    db.commit()
    return True

@app.route("/")
def index():
    cur = get_db().cursor()
    query = """
    SELECT
        m.id,
        m.title,
        m.description,
        m.image,
        GROUP_CONCAT(g.name, ',') AS genres
    FROM movies m
    LEFT JOIN movie_genres mg ON m.id = mg.movie_id
    LEFT JOIN genres g ON mg.genre_id = g.id
    GROUP BY m.id
    """
    cur.execute(query)
    movies = cur.fetchall()
    return render_template("index.html", movies=movies)

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    cur = get_db().cursor()
    cur.execute("""
        SELECT m.id, m.title, m.description, m.image,
               GROUP_CONCAT(g.name, ',') AS genres
        FROM movies m
        LEFT JOIN movie_genres mg ON m.id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        WHERE m.id = ?
        GROUP BY m.id
    """, (movie_id,))
    movie = cur.fetchone()
    if movie:
        return render_template("movie.html", movie=movie)
    else:
        abort(404, description="Film ei leitud")

@app.route("/genre/<genre_name>")
def movies_by_genre(genre_name):
    cur = get_db().cursor()
    query = """
    SELECT
        m.id,
        m.title,
        m.description,
        m.image,
        GROUP_CONCAT(g.name, ',') AS genres
    FROM movies m
    JOIN movie_genres mg ON m.id = mg.movie_id
    JOIN genres g ON mg.genre_id = g.id
    WHERE g.name = ?
    GROUP BY m.id
    """
    cur.execute(query, (genre_name,))
    movies = cur.fetchall()
    if not movies:
        abort(404, description="Žanri filme ei leitud")
    return render_template("genre_movies.html", movies=movies, genre=genre_name)

@app.route("/schedule")
def schedule():
    cur = get_db().cursor()
    query = """
    SELECT
        screenings.id,
        movies.title,
        movies.image,
        cinemas.name AS cinema_name,
        cinemas.location,
        halls.name AS hall_name,
        screenings.start_time,
        screenings.price
    FROM screenings
    JOIN movies ON screenings.movie_id = movies.id
    JOIN halls ON screenings.hall_id = halls.id
    JOIN cinemas ON halls.cinema_id = cinemas.id
    ORDER BY screenings.start_time
    """
    cur.execute(query)
    screenings = cur.fetchall()
    return render_template("schedule.html", screenings=screenings)

@app.route("/buy_ticket/<int:screening_id>", methods=["GET", "POST"])
def buy_ticket(screening_id):
    cur = get_db().cursor()
    cur.execute("""
        SELECT screenings.id, movies.title, screenings.start_time, screenings.price,
               halls.name AS hall_name, cinemas.name AS cinema_name, cinemas.location
        FROM screenings
        JOIN movies ON screenings.movie_id = movies.id
        JOIN halls ON screenings.hall_id = halls.id
        JOIN cinemas ON halls.cinema_id = cinemas.id
        WHERE screenings.id = ?
    """, (screening_id,))
    screening = cur.fetchone()
    if not screening:
        abort(404, description="Ekraanikuva ei leitud")

    if request.method == "POST":
        seat_id = request.form.get("seat_id")
        if not seat_id:
            flash("Palun vali istekoht!", "error")
            return redirect(url_for("buy_ticket", screening_id=screening_id))

        # Proovi osta pilet
        success = buy_ticket_in_db(screening_id, int(seat_id))
        if success:
            flash(f"Pilet edukalt ostetud filmile '{screening['title']}' ({screening['start_time']})!")
            return redirect(url_for("schedule"))
        else:
            flash("Valitud istekoht on juba võetud, palun vali teine.", "error")
            return redirect(url_for("buy_ticket", screening_id=screening_id))

    available_seats = get_available_seats(screening_id)
    taken_seats = get_taken_seats(screening_id)
    return render_template("buy_ticket.html", screening=screening, seats=available_seats, taken_seats=taken_seats)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
