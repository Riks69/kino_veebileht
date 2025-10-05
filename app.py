from flask import Flask, render_template, g, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'movies.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # See võimaldab lugeda tulemusi kui sõnastikke
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


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT id, title, description, image FROM movies")
    movies = cur.fetchall()
    return render_template("index.html", movies=movies)

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    cur = get_db().cursor()
    cur.execute("SELECT id, title, description, image FROM movies WHERE id = ?", (movie_id,))
    movie = cur.fetchone()
    if movie:
        return render_template("movie.html", movie=movie)
    else:
        abort(404, description="Film ei leitud")

if __name__ == "__main__":
    app.run(debug=True)
