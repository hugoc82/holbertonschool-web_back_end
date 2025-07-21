#!/usr/bin/env python3
"""Module that filters sensitive data in log messages."""
import re
import logging
from typing import List


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
