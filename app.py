from flask import Flask, render_template, send_from_directory, session, redirect, url_for
from pathlib import Path

from backend.database import initialize_database
from backend.routes.auth_routes import auth_routes
from backend.routes.user_routes import user_routes
from backend.routes.comments_routes import comments_routes
from backend.routes.search_routes import search_routes

FRONTEND_FOLDER = Path(__file__).resolve().parent / "frontend"

app = Flask(
    __name__,
    template_folder=str(FRONTEND_FOLDER / "templates")
)

# Session configuration
app.secret_key = "vulnerable-portal-secret-key"

app.config["SESSION_COOKIE_HTTPONLY"] = False
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Register API routes
app.register_blueprint(auth_routes, url_prefix="/api")
app.register_blueprint(user_routes, url_prefix="/api")
app.register_blueprint(comments_routes, url_prefix="/api")
app.register_blueprint(search_routes, url_prefix="/api")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        FRONTEND_FOLDER / "images",
        "favicon.ico"
    )


# Frontend routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register_page():

    if "user_id" in session:
        return redirect(url_for("dashboard_page"))

    return render_template("pages/register.html")


@app.route("/login")
def login_page():

    if "user_id" in session:
        return redirect(url_for("dashboard_page"))

    return render_template("pages/login.html")

@app.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    return render_template("pages/dashboard.html")

@app.route("/comments")
def comments_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    return render_template("pages/comments.html")


@app.route("/add_comment")
def add_comment_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    return render_template("pages/add_comment.html")

@app.route("/search")
def search_page():
    return render_template("pages/search.html")


# Static frontend files
@app.route("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(FRONTEND_FOLDER / "css", filename)


@app.route("/js/<path:filename>")
def js_files(filename):
    return send_from_directory(FRONTEND_FOLDER / "js", filename)


if __name__ == "__main__":
    initialize_database()
    app.run(host="127.0.0.1", port=5000, debug=True)
