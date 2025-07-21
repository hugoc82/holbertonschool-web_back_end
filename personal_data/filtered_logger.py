#!/usr/bin/env python3
"""Module that filters sensitive data and manages secure logging/database."""
import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate the values of specified fields in a log message.
    """
    pattern = rf'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, rf'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that obfuscates specified fields in log records.
    """

    REDACTION = "***"
    FORMAT = ("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and obfuscate sensitive fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger configured to redact PII fields from messages.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """
    Connects to a MySQL database using environment variables and returns
    the connection object.
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
