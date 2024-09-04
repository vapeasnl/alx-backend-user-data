#!/usr/bin/env python3
"""Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """GET /api/v1/unauthorized:
    Args:
      Route: GET /api/v1/unauthorized
      This endpoint must raise a 401 error by using abort - Custom Error Pages
      By calling abort(401), the error handler for 401 will be executed.
    """
    abort(401)


@app_views.route('/forbidden/', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """GET /api/v1/forbidden:
    Args:
      Route: GET /api/v1/forbidden
      This endpoint must raise a 403 error by using abort - Custom Error Pages
    Return:
      error": "Forbidden
    """
    abort(403)
