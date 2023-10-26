from pathlib import Path

from project.app import app
import sqlite3

from flask import Flask, g
# connect to database
def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


# open database connection
def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def test_index():
    tester = app.test_client()
    response = tester.get("/", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"Hello, World!"


def test_database():
    assert Path("flaskr.db").is_file()