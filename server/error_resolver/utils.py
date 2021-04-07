import sys

# A list of all standard exeptions
BUILTINS = dir(sys.modules["builtins"])

BASE_URL = "https://api.stackexchange.com/2.2"
SEARCH_URL = BASE_URL + "/search?site=stackoverflow"

HINT_MESSAGES = {
    "KeyError": (
        "<initial_error>\n\nKeyError exceptions are raised to the user when a key is not found in a dictionary."
        "\nTo solve this error you may want to define a key with value <key> in the dictionary."
        "\nOr you may want to use the method .get() of a dictionary which can retrieve the value associated"
        "\nto a key even when the key is missing by passing a default value."
        "\nExample:\n\nfoo = your_dict.get('missing_key', default='bar')"
    ),
    "NameError": (
        "A variable named '<missing_name>' is missing."
        "\nMaybe you forget to define this variable or even you accidentally misspelled its actual name?"
    ),
    "ModuleNotFoundError": (
        "A module (library) named '<missing_module>' is missing."
        "\nYou might want to check if this is a valid module name or"
        "\nif this module can be installed using pip like: 'pip install <missing_module>'"
    ),
    "IndexError": (
        "You tried to access an index that does not exist in a <sequence> at line <line>."
        "\nAn IndexError happens when asking for non existing indexes values of sequences."
        "\nSequences can be lists, tuples and range objects."
        "\nTo fix this make sure that the index value is valid."
    ),
    "SyntaxError": (
        "You have a syntax error somewhere around line <line>"
        "\nGenerally, syntax errors occurs when multiple code statements are interpreted as if they were one."
        "\nThis may be caused by several simple issues, below is a list of them."
        "\nYou should check if your code contains any of these issues."
        "\n"
        "\n1- Make sure that any strings in the code have matching quotation marks."
        "\n2- An unclosed bracket – (, {, or [ – makes Python continue with the next line as part of the current statement."
        "\n   Generally, an error occurs almost immediately in the next line."
        "\n3- Make sure you are not using a Python keyword for a variable name."
        "\n4- Check that you have a colon at the end of the header of every compound statement,"
        "\n   including for, while, if, and def statements."
        "\n5- Check for the classic '=' instead of '==' in a conditional statement."
        "\nSource: https://www.openbookproject.net/thinkcs/python/english2e/app_a.html"
    ),
    "ZeroDivisionError": (
        "You have tried to divide a number by zero around line <line>"
        "\nCheck the division operation to find the error."
        "\nDivision operations where the divisor is generate by a range() can throw this error if the range() starts "
        "at 0. "
    ),
}