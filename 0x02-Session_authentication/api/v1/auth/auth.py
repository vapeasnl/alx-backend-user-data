#!/usr/bin/env python3
"""Module Auth"""

import re
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method def require_auth(self, path: str, excluded_paths:
            List[str]) -> bool: that
            False - path and excluded_paths will be used later, now, you
            don’t need to take care of them
        Return:
            Returns True if path is None
            Returns True if excluded_paths is None or empty
            Returns False if path is in excluded_paths
        Cases:
            You can assume excluded_paths contains string path always
            ending by a / This method must be slash tolerant:
            path=/api/v1/status and path=/api/v1/status/ must be
            returned False if excluded_paths contains /api/v1/status/
        Improve:
            Improve def require_auth(self, path, excluded_paths)
            by allowing * at the end of excluded paths.
            Example for excluded_paths = ["/api/v1/stat*"]:
            /api/v1/users will return True
            /api/v1/status will return False
            /api/v1/stats will return False
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] == "/":
            path = path[:-1]
        for path_excluded in excluded_paths:
            if path_excluded[-1] == "/":
                path_excluded = path_excluded[:-1]
            if path == path_excluded:
                return False
            if path_excluded.endswith("*") and path.startswith(
                path_excluded[:-1]
            ):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method def authorization_header(self, request=None) -> str:
            If request is None, returns None
            If request doesn’t contain the header key Authorization, returns
            None
            Otherwise, return the value of the header request Authorization
        Returns:
            None - request will be the Flask request object
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """public method def current_user(self, request=None) ->
            TypeVar('User'):
        Returns:
            None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """public method def session_cookie(self, request=None):
        Return:
            Return None if request is None
            Return the value of the cookie named _my_session_id from request -
            the name of the cookie must be defined by the environment
            variable SESSION_NAME
        Note:
            You must use .get() built-in for accessing the cookie in
            the request cookies dictionary
            You must use the environment variable SESSION_NAME to define the
            name of the cookie used for the Session ID
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
