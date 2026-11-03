from flask import Blueprint, request, jsonify
import sqlite3

from backend.database import get_db_connection

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    connection = get_db_connection()

    try:

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Account successfully created!"
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "success": False,
            "message": "Username already exists."
        }), 409

    finally:
        connection.close()

@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    connection = get_db_connection()

    try:

        user = connection.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        if user:
            return jsonify({
                "success": True,
                "message": "Login successful!"
            }), 200

        return jsonify({
            "success": False,
            "message": "Invalid username or password."
        }), 401

    finally:
        connection.close()

@auth_routes.route("/user", methods=["GET"])
def get_user():

    username = request.args.get("username")

    if not username:
        return jsonify({
            "success": False,
            "message": "Username is required."
        }), 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            "SELECT id, username FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found."
            }), 404

        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"]
            }
        }), 200

    finally:
        connection.close()