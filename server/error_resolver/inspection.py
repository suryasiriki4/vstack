import re
import sys

from utils import BUILTINS


def get_error_message(error):
    """Extracts the error message from the traceback.
    If no error message is found, will return None.
    Here's an example:

    input:
    Traceback (most recent call last):
    File "example_code.py", line 2, in <module>
        import kivy
    ModuleNotFoundError: No module named 'kivy'

    output:
    ModuleNotFoundError: No module named 'kivy'
    """

    error_lines = error.splitlines()
    return error_lines[-1]

def get_error_type(error_message):
    """Gets the type of the error message and check if it's a valid error
    else return None.
    Here's an example:

    input:
        ModuleNotFoundError: No module named 'kivy'
    output:
        'ModuleNotFoundError'
    """
    error_type = error_message.split(":")[0]
    return error_type

def get_error_line(error):
    """Gets the error line from the compilation message
    Here's an example:
    input:

    Traceback (most recent call last):
    File "example_code.py", line 2, in <module>
        import kivy
    ModuleNotFoundError: No module named 'kivy'

    output:
    2  # <class 'int'>
    """

    # This will match a line like this
    # 'File "foo.py", line 666'
    regex1 = r'File "(.)*", line\s(\d)*'
    # This will match a undefinite number of digits
    # at the end of a string (the error line)
    regex2 = r"([0-9])*$"


    try:
        error_header = re.search(regex1, error)[0]
        error_line = re.search(regex2, error_header)[0]
        return int(error_line)
    except TypeError:
        return None

def get_file_name(error_message):
    """Get the file name where the error originates'
    Here's an example:

    input:
    'File "example_code.py", line 1
        print(
            ^
    SyntaxError: unexpected EOF while parsing'

    output:
    'example_code.py'
    """
    # This will match a line like this
    # 'File "foo.py", line 666'
    regex1 = r'File "(.)*", line\s(\d)*'
    # This will match text between double quotes (file name)
    regex2 = r'"(.)*"'

    try:
        error_header = re.search(regex1, error_message)[0]
        file_name = re.search(regex2, error_header)[0]
        return file_name[1:-1]  # remove double quotes
    except TypeError:
        return None

def get_code(file_path):
    """Gets the source code of the specified file."""
    with open(file_path, "r") as file:
        code = file.read()
    return code

def get_offending_line(error_line, code):
    """Extracts the offending line"""

    error_line -= 1
    code_lines = code.splitlines()
    offending_line = None

    try:
        offending_line = code_lines[error_line]
    except IndexError:
        offending_line = code_lines[-1]

    return offending_line

def inspect_error(error):
    err_msg = get_error_message(error)
    err_msg = err_msg[1:]

    err_typ = get_error_type(err_msg)
    err_line = get_error_line(error)
    err_file_name = get_file_name(error)
    code = get_code(err_file_name)
    offending_line = get_offending_line(err_line, code)

    error_info = {
        "traceback": error,
        "message": err_msg,
        "type": err_typ,
        "line": err_line,
        "file": err_file_name,
        "code": code,
        "offending_line": offending_line,
    }

    return error_info
