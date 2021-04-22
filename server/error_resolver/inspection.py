"""module for inspecting the error source code and the error log."""

import re
import sys

from .err_utils import BUILTINS


def get_error_message(error, programming_language):
    """Extracts the error message from the traceback.
    If no error message is found, will return None.
    Here's an example:

    input:
    Traceback (most recent call last):
    File "sample_code.py", line 2, in <module>
        import tkinter
    ModuleNotFoundError: No module named 'tkinter'

    output:
    ModuleNotFoundError: No module named 'tkinter'
    """

    error_lines = error.splitlines()

    if programming_language == 'node':
        return error_lines[4]
    elif programming_language == 'ruby':
        err_message = error.split(' ')[1:]
        err_message = ' '.join(err_message)
        return err_message
    error_lines[-1] = error_lines[-1][1:]
    return error_lines[-1]

def get_error_type(error_message, programming_language):
    """Gets the type of the error message and check if it's a valid error
    else return None.
    Here's an example:

    input:
        ModuleNotFoundError: No module named 'tkinter'
    output:
        'ModuleNotFoundError'
    """

    if programming_language == "ruby":
        return error_message[error_message.find("(")+1:error_message.find(")")]

    error_type = error_message.split(":")[0]
    return error_type

def get_error_line(error, programming_language):
    """Gets the error line from the compilation message
    Here's an example:
    input:

    Traceback (most recent call last):
    File "sample_code.py", line 2, in <module>
        import tkinter
    ModuleNotFoundError: No module named 'tkinter'

    output:
    2  # <class 'int'>
    """
    if programming_language == 'node':
        splitted_error_lines = error.splitlines()
        error = splitted_error_lines[0]
        num_regex = r"([0-9])*$"
        line_num = re.search(num_regex, error)[0]
        return(int(line_num))
    
    if programming_language == 'ruby':
        error_file_path = error.split(' ')[0]
        line_num = error_file_path.split(':')[-2]
        return int(line_num)

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

def get_file_name(error, programming_language):
    """Get the file name where the error originates'
    Here's an example:

    input:
    'File "sample_code.py", line 1
        print(
            ^
    SyntaxError: unexpected EOF while parsing'

    output:
    'sample_code.py'
    """

    if programming_language == 'node':
        splitted_error_lines = error.splitlines()
        file_path = splitted_error_lines[0].split(':')[0]
        return(file_path)
    
    if programming_language == 'ruby':
        file_path = error.split(' ')[0]
        file_path = file_path.split(':')[0]
        return file_path


    # This will match a line like this
    # 'File "foo.py", line 666'
    regex1 = r'File "(.)*", line\s(\d)*'
    # This will match text between double quotes (file name)
    regex2 = r'"(.)*"'

    try:
        error_header = re.search(regex1, error)[0]
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

def inspect_error(error, programming_language):
    """ 
    summarizies all the error information and returns it as a directory for each traceback of error
    error_info = {
        "traceback": error,
        "message": err_msg,
        "type": err_typ,
        "line": err_line,
        "file": err_file_name,
        "code": code,
        "offending_line": offending_line,
        "prog_lang": programming_language,
    }
    """

    err_msg = get_error_message(error, programming_language)
    err_typ = get_error_type(err_msg, programming_language)
    err_line = get_error_line(error, programming_language)    
    err_file_name = get_file_name(error, programming_language)
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
        "prog_lang": programming_language,
    }

    return error_info
