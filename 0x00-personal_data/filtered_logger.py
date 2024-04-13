#!/usr/bin/env python3
"""
Filtered logger module
"""
from typing import List
import logging
import re


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
    print(pattern)

    return re.sub(pattern,
                  lambda match: f"{match.group().split('=')[0]}={redaction}",
                  message)
