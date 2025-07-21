#!/usr/bin/env python3
"""Module that filters sensitive data in a log message."""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscate the values of specified fields in a log message."""
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*', rf'\1={redaction}', message)
