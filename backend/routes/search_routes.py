from flask import Blueprint, request, jsonify
from backend.database import get_db_connection

search_routes = Blueprint("search", __name__)

@search_routes.route("/search", methods=["GET"])
def search_users():

    username = request.args.get("username", "")

    if not username:
      return jsonify({
        "success": False,
        "message": "Please enter a username to search."
      }), 400

    connection = get_db_connection()

    try:
        query = f"""
            SELECT id, username
            FROM users
            WHERE username LIKE '%{username}%'
        """

        users = connection.execute(query).fetchall()

        return jsonify({
            "success": True,
            "users": [dict(user) for user in users]
        }), 200

    finally:
        connection.close()