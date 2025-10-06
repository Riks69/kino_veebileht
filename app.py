from flask import Flask, render_template, g, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'movies.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Enables dict-like access for rows
    return db

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

@app.route("/")
def index():
    cur = get_db().cursor()
    # Fetch movies with concatenated genres
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
    # Fetch single movie with genres
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
