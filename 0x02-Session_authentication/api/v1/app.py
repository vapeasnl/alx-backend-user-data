#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

AUTH_TYPE = getenv('AUTH_TYPE', 'auth')
if AUTH_TYPE == 'session_auth':
    auth = SessionAuth()
elif AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()
elif AUTH_TYPE == 'auth':
    auth = Auth()


@app.errorhandler(401)
def unauthorized(error):
    """ unauthorized handler:
    Args:
        a JSON: {"error": "Unauthorized"}
        status code 401
        you must use jsonify from Flask
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ forbidden handler:
    Args:
        a JSON: {"error": "Forbidden"}
        status code 403
        you must use jsonify from Flask
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """Method to handle before each request
       if auth is None, do nothing
       if request.path is not part of this list
       ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'],
       do nothing - you must use the method require_auth from the auth instance
       if auth.authorization_header(request) returns None,
       raise the error 401 - you must use abort
       if auth.current_user(request) returns None, raise the
       error 403 - you must use abort
    """
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if not auth.require_auth(request.path, excluded_paths):
            return
        authorization = auth.authorization_header(request)
        session = auth.session_cookie(request)
        if authorization is None and session is None:
            abort(401)
        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)
        request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
