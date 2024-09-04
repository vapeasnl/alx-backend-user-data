#!/usr/bin/env python3
"""View Session Authentication Module"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """You must use request.form.get() to retrieve email and password
        parameters
        If email is missing or empty, return the JSON
        { "error": "email missing" } with the status code 400 If password is
        missing or empty, return the JSON { "error": "password missing" }
        with the status code 400 Retrieve the User instance based on the
        email - you must use the class method search of User
        (same as the one used for the BasicAuth) If no User found,
        return the JSON { "error": "no user found for this email" }
        with the status code 404 If the password is not the one of the
        User found, return the JSON { "error": "wrong password" } with
        the status code 401 - you must use is_valid_password from the
        User instance Otherwise, create a Session ID for the User ID:
        You must use from api.v1.app import auth - WARNING: please import
        it only where you need it - not on top of the file
        (can generate circular import - and break first tasks of this project)
        You must use auth.create_session(..) for creating a Session ID
        Return the dictionary representation of the User - you must use
        to_json() method from User
        You must set the cookie to the response - you must use the
        value of the environment variable SESSION_NAME as cookie name - tip In
        the file api/v1/views/__init__.py, you must add this
        new view at the end of the file.
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def logout():
    """Handles the session logout: Update the class SessionAuth by adding a new
        method def destroy_session(self, request=None): that deletes the user
        session / logout: If the request is equal to None, return False
        If the request doesn’t contain the Session ID cookie, return
        False - you must use self.session_cookie(request) If the
        Session ID of the request is not linked to any User ID, return
        False - you must use self.user_id_for_session_id(...) Otherwise,
        delete in self.user_id_by_session_id the Session ID
        (as key of this dictionary) and return True
    """
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)

    return jsonify({}), 200
