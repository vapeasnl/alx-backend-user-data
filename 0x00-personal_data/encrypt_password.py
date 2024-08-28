#!/usr/bin/env python3
""" Password encryption module """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypts passwords using the bycrpt package """
    if password is None:
        return None
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checks if a password is hashed """
    pwd = password.encode('utf-8')
    if bcrypt.checkpw(pwd, hashed_password):
        return True
    else:
        return False
