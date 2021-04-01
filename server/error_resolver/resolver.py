import sys
import os
import re
import urwid

from queue import Queue
from subprocess import PIPE, Popen
from threading import Thread

import webbrowser

from urwid.widget import (BOX, FLOW, FIXED)

sys.path.append(os.path.abspath('../'))
from tool import search_query


# ASCII codes of colors
GREEN = '\033[92m'
GRAY = '\033[90m'
CYAN = '\033[36m'
RED = '\033[31m'
YELLOW = '\033[33m'
END = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'


# Scroll actions
SCROLL_LINE_UP = "line up"
SCROLL_LINE_DOWN = "line down"
SCROLL_PAGE_UP = "page up"
SCROLL_PAGE_DOWN = "page down"
SCROLL_TO_TOP = "to top"
SCROLL_TO_END = "to end"

# Scrollbar positions
SCROLLBAR_LEFT = "left"
SCROLLBAR_RIGHT = "right"


# getting the language from file path

def get_language(file_path):
    """Returns the language a file is written in."""
    if file_path.endswith(".py"):
        return "python3"
    elif file_path.endswith(".js"):
        return "node"
    elif file_path.endswith(".rb"):
        return "ruby"
    elif file_path.endswith(".cpp"):
        return 'cpp'
    else:
        return '' # Unknown language


# getting the error message

def parse_error(error, language):
    """Filters the stack trace from stderr and returns only the error message."""
    if error == '':
        return None
    elif language == "python3":
        if any(e in error for e in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            return None
        else:
            return error.split('\n')[-2].strip()
    elif language == "node":
        return error.split('\n')[4][1:]
    elif language == "go run":
        return error.split('\n')[1].split(": ", 1)[1][1:]
    elif language == "ruby":
        error_message = error.split('\n')[0]
        return error_message[error_message.rfind(": ") + 2:]
    elif language == "javac":
        m = re.search(r'.*error:(.*)', error.split('\n')[0])
        return m.group(1) if m else None
    elif language == "java":
        for line in error.split('\n'):
            # Multiple error formats
            m = re.search(r'.*(Exception|Error):(.*)', line)
            if m and m.group(2):
                return m.group(2)

            m = re.search(r'Exception in thread ".*" (.*)', line)
            if m and m.group(1):
                return m.group(1)

        return None




# execute the given file

def read(pipe, funcs):
    """Reads and pushes piped output to a shared queue and appropriate lists."""
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line.decode("utf-8"))
    pipe.close()


def write(get):
    """Pulls output from shared queue and prints to terminal."""
    for line in iter(get, None):
        print(line)


## Main ##


def execute(command):
    """Executes a given command and clones stdout/err to both variables and the
    terminal (in real-time)."""
    process = Popen(
        command,
        cwd=None,
        shell=False,
        close_fds=True,
        stdout=PIPE,
        stderr=PIPE,
        bufsize=1
    )

    output, errors = [], []
    pipe_queue = Queue() # Wowee, thanks CS 225

    # Threads for reading stdout and stderr pipes and pushing to a shared queue
    stdout_thread = Thread(target=read, args=(process.stdout, [pipe_queue.put, output.append]))
    stderr_thread = Thread(target=read, args=(process.stderr, [pipe_queue.put, errors.append]))

    writer_thread = Thread(target=write, args=(pipe_queue.get,)) # Thread for printing items in the queue

    # Spawns each thread
    for thread in (stdout_thread, stderr_thread, writer_thread):
        thread.daemon = True
        thread.start()

    process.wait()

    for thread in (stdout_thread, stderr_thread):
        thread.join()

    pipe_queue.put(None)

    output = ' '.join(output)
    errors = ' '.join(errors)

    if "java" != command[0] and not os.path.isfile(command[1]): # File doesn't exist, for java, command[1] is a class name instead of a file
        return (None, None)
    else:
        return (output, errors)


#################<-  Implementing scrollbar  ->####################
############
## INTERFACE
############


## Helper Classes ##


########################
# SCROLLABLE MODULE #
########################

#####################################
# SELCTABLE MODULE #
#####################################


def main():
    programming_language = get_language(sys.argv[1].lower())

    if programming_language == '': # Unknown language
            print("\n%s%s%s" % (RED, "Sorry, resolver doesn't support this file type.\n", END))
            return
    
    file_path = sys.argv[1:]

    output, error = execute([programming_language] + file_path)

    error_message = parse_error(error, programming_language)

    query = "%s %s" % (programming_language, error_message)

    # search_results = []

    search_results = search_query(query)

    # search_results.append({
    #     "index": 0,
    #     "Title": "question number 1",
    #     #"Body": result.find_all("div", class_="excerpt")[0].text,
    #     #"Votes": int(result.find_all("span", class_="vote-count-post ")[0].find_all("strong")[0].text),
    #     "Answers": 1,
    #     "Answer": "sample answer",
    #     "URL": "https://stackoverflow.com/questions/36788688/merge-sort-python-3/36788919"
    # })

    # search_results.append({
    #     "index": 1,
    #     "Title": "question number 2",
    #     #"Body": result.find_all("div", class_="excerpt")[0].text,
    #     #"Votes": int(result.find_all("span", class_="vote-count-post ")[0].find_all("strong")[0].text),
    #     "Answers": 1,
    #     "Answer": "sample answer",
    #     "URL": "https://stackoverflow.com/questions/36788688/merge-sort-python-3/36788919"
    # })

    if confirm("\nDiplay Stack Overflow Results") :
        App(search_results)

       


main()