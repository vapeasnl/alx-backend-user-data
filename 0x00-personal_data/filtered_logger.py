#!/usr/bin/env python3
""" filtered_logger.py """
import re
import logging
import sys
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector import Error
import bcrypt


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter_datum returns the log message obfuscated """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return message


PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """ Initialize the formatter class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        if fields is None:
            self.fields = []
        else:
            self.fields = fields

    def format(self, record: List[str]) -> str:
        """ Formats the logs according to specified criteria """
        format = logging.Formatter.format(self, record)
        format = filter_datum(self.fields, self.REDACTION,
                              format, self.SEPARATOR)
        return format


def get_logger() -> logging.Logger:
    """ Returns a Logging.logger object. Serializes PII fields"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connection to a secure MySQL db """
    try:
        db = os.getenv('PERSONAL_DATA_DB_NAME')
        user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
        password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
        host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')

        connection = mysql.connector.connect(host=host, user=user,
                                             password=password, db=db)
        if connection.is_connected():
            print("Db access Granted!")
        return connection
    except Error as e:
        print(f"Error While connecting to the db: {e}")


def main() -> None:
    """ Create connection to db and retrieve data from the users table """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        if row in PII_FIELDS:
            print(row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
