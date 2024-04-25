import sqlite3
import os
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash,
    abort,
)

# Конфигурация
DATABASE = "/home/andrey/code/flask-projects/flask-first-project/data.db"
DEBUG = True
SECRET_KEY = "fdslkfjdsfkjeuf><FSDJ@#!#!@823492h8fndsjfjhs"

app = Flask(__name__)
app.config.from_object(__name__)

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


@app.route("/")
def index():
    db = get_db()
    return render_template("index.html", menu=[])


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


# menu = [
#     {"name": "Установка", "url": "install-flask"},
#     {"name": "Первое приложение", "url": "first-app"},
#     {"name": "Обратная связь", "url": "contact"},
# ]


# @app.route("/")
# def index():
#     print(url_for("index"))
#     return render_template("index.html", menu=menu)


# @app.route("/about")
# def about():
#     print(url_for("about"))
#     return render_template("about.html", title="О сайте", menu=menu)


# @app.route("/contact", methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         if len(request.form["username"]) > 2:
#             flash("Сообщение отправлено", category="success")
#         else:
#             flash("Ошибка отправки", category="error")

#     return render_template("contact.html", title="Обратная связь", menu=menu)


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if "userLogged" in session:
#         return redirect(url_for("profile", username=session["userLogged"]))
#     elif (
#         request.method == "POST"
#         and request.form["username"] == "andrey"
#         and request.form["psw"] == "123"
#     ):
#         session["userLogged"] = request.form["username"]
#         return redirect(url_for("profile", username=session["userLogged"]))
#     return render_template("login.html", title="Авторизация", menu=menu)


# @app.route("/profile/<username>")
# def profile(username):
#     if "userLogged" not in session or session["userLogged"] != username:
#         abort(401)
#     return f"Профиль пользователя: {username}"


# @app.errorhandler(404)
# def pageNotFound(error):
#     return render_template("page404.html", title="Страница не найдена", menu=menu), 404

if __name__ == "__main__":
    app.run(debug=True)
