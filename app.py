from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'movies.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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
    cur.execute("SELECT title, description, image FROM movies WHERE id = ?", (movie_id,))
    movie = cur.fetchone()
    if movie:
        return render_template("movie.html", movie=movie)
    return "Film ei leitud", 404

if __name__ == "__main__":
    app.run(debug=True)
