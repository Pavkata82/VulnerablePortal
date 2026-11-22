from flask import Blueprint, request, jsonify, session

from backend.database import get_db_connection

comments_routes = Blueprint("comments", __name__)


# GET COMMENTS
@comments_routes.route("/comments", methods=["GET"])
def get_comments():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in."
        }), 401

    connection = get_db_connection()

    try:
        comments = connection.execute("""
            SELECT comments.id, comments.content, users.username
            FROM comments
            JOIN users ON comments.user_id = users.id
            ORDER BY comments.id DESC
        """).fetchall()

        return jsonify({
            "success": True,
            "comments": [dict(comment) for comment in comments]
        }), 200

    finally:
        connection.close()


# ADD COMMENT
@comments_routes.route("/comments", methods=["POST"])
def add_comment():

    print("Session:", dict(session))
    print("Received JSON:", request.get_json(silent=True))

    if "user_id" not in session:
        print("ERROR: User is not logged in.")
        return jsonify({
            "success": False,
            "message": "You must be logged in."
        }), 401


    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "You must be logged in."
        }), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    content = data.get("content", "").strip()

    if not content:
        return jsonify({
            "success": False,
            "message": "Comment content is required."
        }), 400

    connection = get_db_connection()

    try:
        connection.execute(
            "INSERT INTO comments (user_id, content) VALUES (?, ?)",
            (session["user_id"], content)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Comment successfully posted!"
        }), 201

    finally:
        connection.close()