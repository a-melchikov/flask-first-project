import datetime
import sqlite3
import os
from flask import (
    Flask,
    abort,
    flash,
    g,
    make_response,
    render_template,
    request,
    session,
)
from FDataBase import FDataBase

# Конфигурация
DATABASE = "/home/andrey/code/flask-projects/flask-first-project/data.db"
DEBUG = True
SECRET_KEY = "b1670b8fc8f5c511a53e5c4363f733f9419802e2"

app = Flask(__name__)
app.config.from_object(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=10)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "data.db")))


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


# @app.route("/")
# def index():
#     db = get_db()
#     dbase = FDataBase(db)
#     return render_template(
#         "index.html", menu=dbase.getMenu(), posts=dbase.getPostsAnonce()
#     )


@app.route("/")
def index():
    if "visits" in session:
        session["visits"] = session.get("visits") + 1
    else:
        session["visits"] = 1
    return f"<h1>Main Page</h1><p>Число просмотров: {session['visits']}"


data = [1, 2, 3, 4]


@app.route("/session")
def session_data():
    session.permanent = True
    if "data" not in session:
        session["data"] = data
    else:
        session["data"][1] += 1
        session.modified = True
    return f"<p>session['data']: {session['data']}"


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form["name"]) > 4 and len(request.form["post"]) > 10:
            res = dbase.addPost(
                request.form["name"], request.form["post"], request.form["url"]
            )
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")
    return render_template(
        "add_post.html", menu=dbase.getMenu(), title="Добавление статьи"
    )


@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template("post.html", menu=dbase.getMenu(), title=title, post=post)


@app.route("/login")
def login():
    log = ""
    if request.cookies.get("logged"):
        log = request.cookies.get("logged")

    res = make_response(f"<h1>Форма авторизации</h1><p>logged: {log}")
    res.set_cookie("logged", "yes", 30 * 24 * 3600)
    return res


@app.route("/logout")
def logout():
    res = make_response("<p>Вы больше не авторизованы!</p>")
    res.set_cookie("logged", "", 0)
    return res


if __name__ == "__main__":
    app.run(debug=True)
