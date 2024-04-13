#!/usr/bin/env python3
"""
Filtered logger module
"""
from typing import List
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log using filter_datum
        """
        message = super(RedactingFormatter, self).format(record)

        return filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR
        )


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Returns the log message obfuscated
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]+"

    return re.sub(pattern,
                  lambda match: f"{match.group().split('=')[0]}={redaction}",
                  message)


def get_logger() -> logging.Logger:
    """
    Logs users
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[stream_handler]
    )

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger
