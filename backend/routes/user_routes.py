from flask import Blueprint, request, jsonify, session

from backend.database import get_db_connection

user_routes = Blueprint("users", __name__)


# GET USER INFORMATION (INTENTIONALLY VULNERABLE TO IDOR)
@user_routes.route("/user", methods=["GET"])
def get_user():

    # Check whether the user is logged in
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in."
        }), 401

    # Get username from URL query parameter
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