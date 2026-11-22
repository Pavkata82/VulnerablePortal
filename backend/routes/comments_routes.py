from flask import Blueprint, request, jsonify
import sqlite3

from backend.database import get_db_connection

comments_routes = Blueprint("comments", __name__)

@comments_routes.route("/comments", methods=["GET"])
def get_comments():

  connection = get_db_connection()

  try:
  
    comments = connection.execute(
       "SELECT * FROM comments"
       ).fetchall()

    return jsonify({
            "success": True,
            "comments": [
                dict(comment) for comment in comments
            ]
        }), 200

  except sqlite3.IntegrityError:

      return jsonify({
          "success": False,
          "message": "Unable to fetch comments."
      }), 404

  finally:
      connection.close()

@comments_routes.route("/comments", methods=["POST"])
def add_comment():

  data = request.get_json(silent=True)
  
  if not data:
      return jsonify({
          "success": False,
          "message": "Invalid request data."
      }), 400

  username = data.get("username", "").strip()
  content = data.get("content", "")

  if not username or not content:
      return jsonify({
          "success": False,
          "message": "Username and content is required."
      }), 400

  connection = get_db_connection()

  try:
  
    connection.execute(
        "INSERT INTO comments (username, content) VALUES (?, ?)",
        (username, content)
    )

    connection.commit()

    return jsonify({
        "success": True,
        "message": "Comment successfully posted!"
    }), 201

  except sqlite3.IntegrityError:
    return jsonify({
        "success": False,
        "message": "Unable to post comments."
    }), 404
  
  finally:
    connection.close()