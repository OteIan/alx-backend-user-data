#!/usr/bin/env python3
"""
Filtered logger module
"""
from typing import List
import os
import re
import logging
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to a database
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        port=3306,
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME", "")
    )


def main():
    """
    Logs the info on a table
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    query = f"SELECT {fields} from users;"
    columns = fields.split(',')
    info_logger = get_logger()
    connection = get_db()

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            record = map(lambda i: f"{i[0]}={i[1]}", zip(columns, row))

            message = f"{'; '.join(list(record))};"
            args = ("user_data", logging.INFO, None, None, message, None, None)

            logRecord = logging.LogRecord(*args)
            info_logger.handle(logRecord)


if __name__ == "__main__":
    main()
