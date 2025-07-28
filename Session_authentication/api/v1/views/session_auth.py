#!/usr/bin/env python3
"""
View for Session Authentication
"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handle user login by creating a Session ID and setting it in a cookie.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Email missing
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    # Password missing
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Check password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth here to avoid circular imports
    from api.v1.app import auth
    # Create a session ID for this user
    session_id = auth.create_session(user.id)

    # Build the response with the user data
    response = make_response(jsonify(user.to_json()))

    # Set the cookie
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """
    DELETE /auth_session/logout
    Deletes the user session / log out.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
