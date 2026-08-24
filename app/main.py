from flask import Flask, jsonify, render_template, request
from neo4j.exceptions import Neo4jError, ServiceUnavailable
from .db import get_driver, verify, close
from .queries import SEARCH_MOVIES, MOVIE_DETAILS, RECOMMEND, TWO_HOP, TOP_GENRES
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure Flask to use the project's templates and static folders
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


def run(query, **params):
    with get_driver().session() as session:
        return [record.data() for record in session.run(query, **params)]


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        verify()
        return jsonify({
            "ok": True,
            "message": "CognoDB connection is healthy."
        })
    except Exception as exc:
        return jsonify({
            "ok": False,
            "message": str(exc)
        }), 503


@app.get("/api/movies")
def movies():
    q = request.args.get("q", "").strip()

    if not q:
        return jsonify([])

    try:
        return jsonify(run(SEARCH_MOVIES, q=q))
    except (Neo4jError, ServiceUnavailable, RuntimeError) as exc:
        return jsonify({
            "error": str(exc)
        }), 503


@app.get("/api/movie/<path:title>")
def movie(title):
    try:
        rows = run(MOVIE_DETAILS, title=title)

        if not rows:
            return jsonify({
                "error": "Movie not found"
            }), 404

        return jsonify(rows[0])

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 503


@app.get("/api/recommendations")
def recommendations():
    title = request.args.get("title", "").strip()

    if not title:
        return jsonify({
            "error": "title is required"
        }), 400

    try:
        return jsonify(run(RECOMMEND, title=title))

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 503


@app.get("/api/two-hop")
def two_hop():
    title = request.args.get("title", "").strip()

    if not title:
        return jsonify({
            "error": "title is required"
        }), 400

    try:
        return jsonify(run(TWO_HOP, title=title))

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 503


@app.get("/api/genres")
def genres():
    try:
        return jsonify(run(TOP_GENRES))

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 503


@app.teardown_appcontext
def teardown(_exception):
    pass


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

