
from flask import Flask, render_template, send_from_directory
from pathlib import Path

from backend.database import initialize_database
from backend.routes.auth_routes import auth_routes
from backend.routes.comments_routes import comments_routes

FRONTEND_FOLDER = Path(__file__).resolve().parent / "frontend"

app = Flask(
    __name__,
    template_folder=str(FRONTEND_FOLDER / "templates")
)

# Register API routes
app.register_blueprint(auth_routes, url_prefix="/api")
app.register_blueprint(comments_routes, url_prefix="/api")


# Frontend routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("pages/register.html")


@app.route("/login")
def login_page():
    return render_template("pages/login.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("pages/dashboard.html")

@app.route("/comments")
def comments_page():
    return render_template("pages/comments.html")

@app.route("/add_comment")
def add_comment_page():
    return render_template("pages/add_comment.html")


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
