#!/usr/bin/env python3
"""Module BasicAuth"""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth"""
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extracts base64 authorization header:
            class BasicAuth that returns the Base64 part of the Authorization
            header for a Basic Authentication:
        Return:
            Return None if authorization_header is None
            Return None if authorization_header is not a string
            Return None if authorization_header doesn’t start by Basic
            (with a space at the end)
            Otherwise, return the value after Basic (after the space)
            You can assume authorization_header contains only one Basic
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decoded_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decodes base64 authorization header:
            class BasicAuth that returns the decoded value of a Base64
            string base64_authorization_header:
        Return:
            Return None if base64_authorization_header is None
            Return None if base64_authorization_header is not a string
            Return None if base64_authorization_header is not a valid
            Base64 - you can use try/except Otherwise, return the decoded
            value as UTF8 string - you can use decode('utf-8')
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_bytes = base64.b64decode(base64_authorization_header)
            return decode_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extracts user credentials: class BasicAuth that returns
            the user email and password from the Base64 decoded value.
        Return:
            This method must return 2 values
            Return None, None if decoded_base64_authorization_header is None
            Return None, None if decoded_base64_authorization_header
            is not a string
            Return None, None if decoded_base64_authorization_header
            doesn’t contain:
            Otherwise, return the user email and the user password - these 2
            values must be separated by a : You can assume
            decoded_base64_authorization_header will contain only one:
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = (
            decoded_base64_authorization_header.split(":", 1)
        )
        return user_email, user_password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Returns a user object from user credentials: class BasicAuth that
            returns the User instance based on his email and password.
        Return:
            Return None if user_email is None or not a string
            Return None if user_pwd is None or not a string
            Return None if your database (file) doesn’t contain any
            User instance with email equal to user_email - you should
            use the class method search of the User to lookup the list of
            users based on their email. Don’t forget to test all cases:
            “what if there is no user in DB?”, etc.
            Return None if user_pwd is not the password of the User
            instance found - you must use the method is_valid_password of User
            Otherwise, return the User instance
        """
        if user_email is None or type(user_email) != str or\
           user_pwd is None or type(user_pwd) != str:\

            return None

        try:
            exist_user: List[TypeVar('User')]
            exist_user = User.search({"email": user_email})
        except Exception:
            return None

        for user in exist_user:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user based on the Authorization
            header of the: the class BasicAuth that overloads
            Auth and retrieves the User instance for a request:
        Return:
            You must use authorization_header
            You must use extract_base64_authorization_header
            You must use decoded_base64_authorization_header
            You must use extract_user_credentials
            You must use user_object_from_credentials
        Note:
            With this update, now your API is fully
            protected by a Basic Authentication. Enjoy!
        """
        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return None
        base64_authorization_header = (
            self.extract_base64_authorization_header(authorization_header)
        )
        if not base64_authorization_header:
            return None
        user_credentials = (
            self.decoded_base64_authorization_header(
                base64_authorization_header
            )
        )
        if not user_credentials:
            return None
        user_email, user_pwd = self.extract_user_credentials(user_credentials)
        if not user_email or not user_pwd:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
