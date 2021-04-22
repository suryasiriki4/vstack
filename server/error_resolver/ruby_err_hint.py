"""
this module handles the code errors of ruby programming language:
1. It gives the query to be used for stackoveflow api.
2. It also gives the local hints for that specific error which changes dynamically.
"""

import re

from typing import List, Union
from argparse import Namespace

from slugify import slugify

from .err_utils import ERR_HINT_MESSAGES, SEARCH_URL

from .err_utils import (
    SINGLE_QUOTE_CHAR,
    SINGLE_SPACE_CHAR,
    EMPTY_STRING,
)


def handle_error_ruby(error_info: dict) -> tuple:

    pycee_hint = None

    error_type = error_info["type"]
    error_message = error_info["message"]
    error_line = error_info["line"]

    print("\nHINTS FROM vstool :\n")
    print("*" * 40)
    print(error_type)

    if error_type == "NameError":
        pycee_hint = handle_name_error_locally(error_message)
        query = handle_name_error(error_message)

    return query, pycee_hint
    

def handle_name_error_locally(error_message: str) -> str:
    """When NameError is handled locally we ask if the user
    accidentally forget to define a variable or misspelled its name."""

    missing_name = get_quoted_words(error_message)[0]
    hint = ERR_HINT_MESSAGES["NameError"].replace("<missing_name>", missing_name)
    return hint

def handle_name_error(error_message: str) -> str:
    """Process an NameError by removing the variable name.
    By doing this the default error can be search without interference
    of the variable name, which does not add to the problem.
    example:
    input:
        "NameError: name 'a' is not defined"
    output:
        "NameError: name is not defined"
    """
    return url_for_error(remove_quoted_words(error_message))

def get_query_params(error_message: str) -> str:
    """Prepares the query to include necessary filters and meet URL format."""

    print(error_message)

    error_message_slug = slugify(error_message, separator="+")
    order = "&order=desc"
    sort = "&sort=relevance"
    python_tagged = "&tagged=ruby"
    intitle = f"&intitle={error_message_slug}"

    return order + sort + python_tagged + intitle

def url_for_error(error_message: str) -> str:
    """Build a valid search url."""

    return SEARCH_URL + get_query_params(error_message)


def remove_quoted_words(error_message: str) -> str:
    """Removes quoted words from an error message.
    Example:
    input: "NameError: name 'a' is not defined"
    output: "NameError: name is not defined"
    """
    return re.sub(r"`.*?'", EMPTY_STRING, error_message)

def get_quoted_words(error_message: str) -> List[str]:
    """Extract words surrounded by single quotes.
    Example:
    input: "AttributeError: 'int' object has no attribute 'append'"
    output: ['int', 'append']
    """
    return error_message.split(SINGLE_QUOTE_CHAR)[1::2]