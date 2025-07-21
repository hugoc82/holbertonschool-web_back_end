#!/usr/bin/env python3
"""Module that filters sensitive data in log messages."""
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate the values of specified fields in a log message.
    """
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*', rf'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that obfuscates specified fields in log records.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
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
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)
