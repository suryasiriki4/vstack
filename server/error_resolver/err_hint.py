"""Contains all the logic that handles code errors."""
import re
from typing import List, Union
from argparse import Namespace

from slugify import slugify

from utils import HINT_MESSAGES, SEARCH_URL

def handle_error(error_info: dict) -> tuple:
    """Process the incoming error as needed and outputs three possible answer.
    output:
    query: an URL containing an stackoverflow query about the error.
    err_hint: A possible answer for the error produced locally.
    TODO: pydoc_answer: A possible answer extracted from the builtin help.
    """

    pydoc_answer = None
    err_hint = None
    error_type = error_info["type"]
    error_message = error_info["message"]
    error_line = error_info["line"]

    if error_type == "SyntaxError":
        err_hint = handle_syntax_error_locally(error_message, error_line)
        query = handle_syntax_error(error_message)

    elif error_type == "TabError":
        query = handle_tab_error(error_message)

    elif error_type == "IndentationError":
        query = handle_indentation_error(error_message)

    elif error_type == "IndexError":
        err_hint = handle_index_error_locally(error_message, error_line)
        query = handle_index_error(error_message)

    elif error_type == "ModuleNotFoundError":
        err_hint = handle_module_error_locally(error_message)
        query = handle_module_not_found_error(error_message)

    elif error_type == "TypeError":
        query = handle_type_error(error_message)

    elif error_type == "KeyError":
        err_hint = handle_key_error_locally(error_message, error_info["offending_line"])
        query = handle_key_error(error_message)

    elif error_type == "AttributeError":
        query = handle_attr_error(error_message)

    elif error_type == "NameError":
        err_hint = handle_name_error_locally(error_message)
        query = handle_name_error(error_message)

    elif error_type == "ZeroDivisionError":
        err_hint = handle_zero_division_error_locally(error_line)
        query = handle_zero_division_error(error_message)

    else:
        query = url_for_error(error_message)  # default query

    print(err_hint)

    return query, err_hint

def handle_syntax_error_locally(error_message: str, error_line: int) -> Union[str, None]:
    """ Process a SyntaxError locally """

    answer = None
    if error_message == "SyntaxError: invalid syntax":
        answer = HINT_MESSAGES["SyntaxError"].replace("<line>", str(error_line))

    return answer

def handle_syntax_error(error_message: str) -> Union[str, None]:
    """Process a SyntaxError """

    # if a generic SyntaxError happens
    # it's quite tricky to catch the right offending line
    if error_message == "SyntaxError: invalid syntax":
        return None
    else:
        error = slugify(error_message, separator="+")
        return url_for_error(error)

def handle_key_error_locally(error_message: str, offending_line: str) -> str:
    """When KeyError is handled locally we remind the user that the problematic
    dict should have a key with a certain value."""

    missing_key = error_message.split(SINGLE_SPACE_CHAR, maxsplit=1)[-1]

    # this first regex will match part of the pattern of a dict acess: a_dict[some_value]
    dict_acess_regex = r"[A-Za-z_]\w*\["
    # this second regex will match only the identifier of the problematic dictionaries
    identifier_regex = r"[A-Za-z_]\w*"

    acesses = re.findall(dict_acess_regex, offending_line)
    indentifiers = [re.findall(identifier_regex, a)[0] for a in acesses]

    # when offending line deals with only the same problematic dictionary
    # we can assert a better error message
    # else when offending line contains different dictionaries with same missing key,
    # we cannot determine which dict originated the error.
    target = indentifiers[0] if len(set(indentifiers)) == 1 else None

    hint = define_hint_for_key_error_locally(target, missing_key, indentifiers)

    return hint


# Helper methods below


def set_pagesize(query: str, pagesize: int) -> str:
    """Set the number of questions we want from Stackoverflow."""
    return query + f"&pagesize={pagesize}"


def get_query_params(error_message: str) -> str:
    """Prepares the query to include necessary filters and meet URL format."""

    error_message_slug = slugify(error_message, separator="+")
    order = "&order=desc"
    sort = "&sort=relevance"
    python_tagged = "&tagged=python"
    intitle = f"&intitle={error_message_slug}"

    return order + sort + python_tagged + intitle


def url_for_error(error_message: str) -> str:
    """Build a valid search url."""

    return SEARCH_URL + get_query_params(error_message)

