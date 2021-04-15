import sys
import os
import re
import urwid
import importlib

from queue import Queue
from subprocess import PIPE, Popen
from threading import Thread

import webbrowser

from urwid.widget import (BOX, FLOW, FIXED)

from inspection import inspect_error
from err_hint import handle_error

from ..tool import search_query

# sys.path.append(os.path.abspath("/home/"))
# from  ..summariser import sumy
# from sumy import get_summarised_answer


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


class Scrollable(urwid.WidgetDecoration):
    # TODO: Fix scrolling behavior (works with up/down keys, not with cursor)

    def sizing(self):
        return frozenset([BOX,])


    def selectable(self):
        return True


    def __init__(self, widget):
        """Box widget (wrapper) that makes a fixed or flow widget vertically scrollable."""
        self._trim_top = 0
        self._scroll_action = None
        self._forward_keypress = None
        self._old_cursor_coords = None
        self._rows_max_cached = 0
        self._rows_max_displayable = 0
        self.__super.__init__(widget)


    def render(self, size, focus=False):
        maxcol, maxrow = size

        # Render complete original widget
        ow = self._original_widget
        ow_size = self._get_original_widget_size(size)
        canv = urwid.CompositeCanvas(ow.render(ow_size, focus))
        canv_cols, canv_rows = canv.cols(), canv.rows()

        if canv_cols <= maxcol:
            pad_width = maxcol - canv_cols
            if pad_width > 0: # Canvas is narrower than available horizontal space
                canv.pad_trim_left_right(0, pad_width)

        if canv_rows <= maxrow:
            fill_height = maxrow - canv_rows
            if fill_height > 0: # Canvas is lower than available vertical space
                canv.pad_trim_top_bottom(0, fill_height)
        self._rows_max_displayable = maxrow
        if canv_cols <= maxcol and canv_rows <= maxrow: # Canvas is small enough to fit without trimming
            return canv

        self._adjust_trim_top(canv, size)

        # Trim canvas if necessary
        trim_top = self._trim_top
        trim_end = canv_rows - maxrow - trim_top
        trim_right = canv_cols - maxcol
        if trim_top > 0:
            canv.trim(trim_top)
        if trim_end > 0:
            canv.trim_end(trim_end)
        if trim_right > 0:
            canv.pad_trim_left_right(0, -trim_right)

        # Disable cursor display if cursor is outside of visible canvas parts
        if canv.cursor is not None:
            curscol, cursrow = canv.cursor
            if cursrow >= maxrow or cursrow < 0:
                canv.cursor = None

        # Let keypress() know if original_widget should get keys
        self._forward_keypress = bool(canv.cursor)

        return canv


    def keypress(self, size, key):
        if self._forward_keypress:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)

            # Remember previous cursor position if possible
            if hasattr(ow, "get_cursor_coords"):
                self._old_cursor_coords = ow.get_cursor_coords(ow_size)

            key = ow.keypress(ow_size, key)
            if key is None:
                return None

        # Handle up/down, page up/down, etc
        command_map = self._command_map
        if command_map[key] == urwid.CURSOR_UP:
            self._scroll_action = SCROLL_LINE_UP
        elif command_map[key] == urwid.CURSOR_DOWN:
            self._scroll_action = SCROLL_LINE_DOWN
        elif command_map[key] == urwid.CURSOR_PAGE_UP:
            self._scroll_action = SCROLL_PAGE_UP
        elif command_map[key] == urwid.CURSOR_PAGE_DOWN:
            self._scroll_action = SCROLL_PAGE_DOWN
        elif command_map[key] == urwid.CURSOR_MAX_LEFT: # "home"
            self._scroll_action = SCROLL_TO_TOP
        elif command_map[key] == urwid.CURSOR_MAX_RIGHT: # "end"
            self._scroll_action = SCROLL_TO_END
        else:
            return key

        self._invalidate()


    def mouse_event(self, size, event, button, col, row, focus):
        ow = self._original_widget
        if hasattr(ow, "mouse_event"):
            ow_size = self._get_original_widget_size(size)
            row += self._trim_top
            return ow.mouse_event(ow_size, event, button, col, row, focus)
        else:
            return False


    def _adjust_trim_top(self, canv, size):
        """Adjust self._trim_top according to self._scroll_action"""
        action = self._scroll_action
        self._scroll_action = None

        maxcol, maxrow = size
        trim_top = self._trim_top
        canv_rows = canv.rows()

        if trim_top < 0:
            # Negative trim_top values use bottom of canvas as reference
            trim_top = canv_rows - maxrow + trim_top + 1

        if canv_rows <= maxrow:
            self._trim_top = 0  # Reset scroll position
            return

        def ensure_bounds(new_trim_top):
            return max(0, min(canv_rows - maxrow, new_trim_top))

        if action == SCROLL_LINE_UP:
            self._trim_top = ensure_bounds(trim_top - 1)
        elif action == SCROLL_LINE_DOWN:
            self._trim_top = ensure_bounds(trim_top + 1)
        elif action == SCROLL_PAGE_UP:
            self._trim_top = ensure_bounds(trim_top - maxrow+1)
        elif action == SCROLL_PAGE_DOWN:
            self._trim_top = ensure_bounds(trim_top + maxrow-1)
        elif action == SCROLL_TO_TOP:
            self._trim_top = 0
        elif action == SCROLL_TO_END:
            self._trim_top = canv_rows - maxrow
        else:
            self._trim_top = ensure_bounds(trim_top)

        if self._old_cursor_coords is not None and self._old_cursor_coords != canv.cursor:
            self._old_cursor_coords = None
            curscol, cursrow = canv.cursor
            if cursrow < self._trim_top:
                self._trim_top = cursrow
            elif cursrow >= self._trim_top + maxrow:
                self._trim_top = max(0, cursrow - maxrow + 1)


    def _get_original_widget_size(self, size):
        ow = self._original_widget
        sizing = ow.sizing()
        if FIXED in sizing:
            return ()
        elif FLOW in sizing:
            return (size[0],)


    def get_scrollpos(self, size=None, focus=False):
        return self._trim_top


    def set_scrollpos(self, position):
        self._trim_top = int(position)
        self._invalidate()


    def rows_max(self, size=None, focus=False):
        if size is not None:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)
            sizing = ow.sizing()
            if FIXED in sizing:
                self._rows_max_cached = ow.pack(ow_size, focus)[1]
            elif FLOW in sizing:
                self._rows_max_cached = ow.rows(ow_size, focus)
            else:
                raise RuntimeError("Not a flow/box widget: %r" % self._original_widget)
        return self._rows_max_cached

    @property
    def scroll_ratio(self):
        return self._rows_max_cached / self._rows_max_displayable


##########################################################################
# SCROLLBAR CLASS MODULE #
##########################################################################
class ScrollBar(urwid.WidgetDecoration):
    # TODO: Change scrollbar size and color(?)

    def sizing(self):
        return frozenset((BOX,))


    def selectable(self):
        return True


    def __init__(self, widget, thumb_char=u'\u2588', trough_char=' ',
                 side=SCROLLBAR_RIGHT, width=1):
        """Box widget that adds a scrollbar to `widget`."""
        self.__super.__init__(widget)
        self._thumb_char = thumb_char
        self._trough_char = trough_char
        self.scrollbar_side = side
        self.scrollbar_width = max(1, width)
        self._original_widget_size = (0, 0)
        self._dragging = False


    def render(self, size, focus=False):
        maxcol, maxrow = size

        ow = self._original_widget
        ow_base = self.scrolling_base_widget
        ow_rows_max = ow_base.rows_max(size, focus)
        if ow_rows_max <= maxrow: # Canvas fits without scrolling - no scrollbar needed
            self._original_widget_size = size
            return ow.render(size, focus)

        sb_width = self._scrollbar_width
        self._original_widget_size = ow_size = (maxcol-sb_width, maxrow)
        ow_canv = ow.render(ow_size, focus)

        pos = ow_base.get_scrollpos(ow_size, focus)
        posmax = ow_rows_max - maxrow

        # Thumb shrinks/grows according to the ratio of
        # <number of visible lines> / <number of total lines>
        thumb_weight = min(1, maxrow / max(1, ow_rows_max))
        thumb_height = max(1, round(thumb_weight * maxrow))

        # Thumb may only touch top/bottom if the first/last row is visible
        top_weight = float(pos) / max(1, posmax)
        top_height = int((maxrow-thumb_height) * top_weight)
        if top_height == 0 and top_weight > 0:
            top_height = 1

        # Bottom part is remaining space
        bottom_height = maxrow - thumb_height - top_height
        assert thumb_height + top_height + bottom_height == maxrow

        # Create scrollbar canvas
        top = urwid.SolidCanvas(self._trough_char, sb_width, top_height)
        thumb = urwid.SolidCanvas(self._thumb_char, sb_width, thumb_height)
        bottom = urwid.SolidCanvas(self._trough_char, sb_width, bottom_height)
        sb_canv = urwid.CanvasCombine([
            (top, None, False),
            (thumb, None, False),
            (bottom, None, False),
        ])

        combinelist = [(ow_canv, None, True, ow_size[0]), (sb_canv, None, False, sb_width)]
        if self._scrollbar_side != SCROLLBAR_LEFT:
            return urwid.CanvasJoin(combinelist)
        else:
            return urwid.CanvasJoin(reversed(combinelist))


    @property
    def scrollbar_width(self):
        return max(1, self._scrollbar_width)


    @scrollbar_width.setter
    def scrollbar_width(self, width):
        self._scrollbar_width = max(1, int(width))
        self._invalidate()


    @property
    def scrollbar_side(self):
        return self._scrollbar_side


    @scrollbar_side.setter
    def scrollbar_side(self, side):
        if side not in (SCROLLBAR_LEFT, SCROLLBAR_RIGHT):
            raise ValueError("scrollbar_side must be 'left' or 'right', not %r" % side)
        self._scrollbar_side = side
        self._invalidate()


    @property
    def scrolling_base_widget(self):
        """Nearest `base_widget` that is compatible with the scrolling API."""
        def orig_iter(w):
            while hasattr(w, "original_widget"):
                w = w.original_widget
                yield w
            yield w

        def is_scrolling_widget(w):
            return hasattr(w, "get_scrollpos") and hasattr(w, "rows_max")

        for w in orig_iter(self):
            if is_scrolling_widget(w):
                return w

    @property
    def scrollbar_column(self):
        if self.scrollbar_side == SCROLLBAR_LEFT:
            return 0
        if self.scrollbar_side == SCROLLBAR_RIGHT:
            return self._original_widget_size[0]

    def keypress(self, size, key):
        return self._original_widget.keypress(self._original_widget_size, key)


    def mouse_event(self, size, event, button, col, row, focus):
        ow = self._original_widget
        ow_size = self._original_widget_size
        handled = False
        if hasattr(ow, "mouse_event"):
            handled = ow.mouse_event(ow_size, event, button, col, row, focus)

        if not handled and hasattr(ow, "set_scrollpos"):
            if button == 4: # Scroll wheel up
                pos = ow.get_scrollpos(ow_size)
                if pos > 0:
                    ow.set_scrollpos(pos - 1)
                    return True
            elif button == 5: # Scroll wheel down
                pos = ow.get_scrollpos(ow_size)
                ow.set_scrollpos(pos + 1)
                return True
            elif col == self.scrollbar_column:
                ow.set_scrollpos(int(row*ow.scroll_ratio))
                if event == "mouse press":
                    self._dragging = True
                elif event == "mouse release":
                    self._dragging = False
            elif self._dragging:
                ow.set_scrollpos(int(row*ow.scroll_ratio))
                if event == "mouse release":
                    self._dragging = False



        return False
##########################################################################
# SELCTABLE MODULE #
##########################################################################
##################################################################################
class SelectableText(urwid.Text):
    def selectable(self):
        return True


    def keypress(self, size, key):
        return key

# helper function
def interleave(a, b):
    result = []
    while a and b:
        result.append(a.pop(0))
        result.append(b.pop(0))

    result.extend(a)
    result.extend(b)

    return result

class App(object):
    def __init__(self, search_results):
        self.search_results, self.viewing_answers = search_results, False
        self.palette = [
            ("title", "light cyan,bold", "default", "standout"),
            ("stats", "light green", "default", "standout"),
            ("menu", "black", "light cyan", "standout"),
            ("reveal focus", "black", "light cyan", "standout"),
            ("reveal viewed focus", "yellow, bold", "light cyan", "standout"),
            ("no answers", "light red", "default", "standout"),
            ("code", "brown", "default", "standout"),
            ("viewed", "yellow", "default", "standout")
        ]
        self.menu = urwid.Text([
            u'\n',
            ("menu", u" ENTER "), ("light gray", u" View answers "),
            ("menu", u" B "), ("light gray", u" Open browser "),
            ("menu", u" Q "), ("light gray", u" Quit"),
        ])

        results = list(map(lambda result: urwid.AttrMap(SelectableText(self._stylize_title(result)), None, "reveal focus"), self.search_results)) # TODO: Add a wrap='clip' attribute
        self.content = urwid.SimpleListWalker(results)
        self.content_container = urwid.ListBox(self.content)
        layout = urwid.Frame(body=self.content_container, footer=self.menu)

        self.main_loop = urwid.MainLoop(layout, self.palette, unhandled_input=self._handle_input)
        self.original_widget = self.main_loop.widget

        self.main_loop.run()


    def _handle_input(self, input):
        if input == "enter" or (input[0]=='meta mouse press' and input[1]==1): # View answers   Either press Enter or "ALT + Left Click"
            url = self._get_selected_link()

            if url != None:
                self.viewing_answers = True
                question_title, question_desc, question_stats, answers = get_question_and_answers(url)

                pile = urwid.Pile(self._stylize_question(question_title, question_desc, question_stats) + [urwid.Divider('*')] +
                interleave(answers, [urwid.Divider('-')] * (len(answers) - 1)))
                padding = ScrollBar(Scrollable(urwid.Padding(pile, left=2, right=2)))
                #filler = urwid.Filler(padding, valign="top")
                linebox = urwid.LineBox(padding)

                menu = urwid.Text([
                    u'\n',
                    ("menu", u" ESC "), ("light gray", u" Go back "),
                    ("menu", u" B "), ("light gray", u" Open browser "),
                    ("menu", u" Q "), ("light gray", u" Quit"),
                ])

                # highlight the selected answer
                _, idx = self.content_container.get_focus()
                txt = self.content[idx].original_widget.text
                self.content[idx] = urwid.AttrMap(SelectableText(txt), 'viewed', 'reveal viewed focus')

                self.main_loop.widget = urwid.Frame(body=urwid.Overlay(linebox, self.content_container, "center", ("relative", 60), "middle", 23), footer=menu)
        elif input in ('b', 'B') or (input[0]=='ctrl mouse press' and input[1]==1): # Open link     Either press (B or b) or "CTRL + Left Click"
            url = self._get_selected_link()

            if url != None:
                webbrowser.open(url)
        elif input == "esc": # Close window
            if self.viewing_answers:
                self.main_loop.widget = self.original_widget
                self.viewing_answers = False
            else:
                raise urwid.ExitMainLoop()
        elif input in ('q', 'Q'): # Quit
            raise urwid.ExitMainLoop()


    def _get_selected_link(self):
        focus_widget, idx = self.content_container.get_focus() # Gets selected item
        title = focus_widget.base_widget.text

        for result in self.search_results:
            if title == self._stylize_title(result): # Found selected title's search_result dict
                return result["URL"]


    def _stylize_title(self, search_result):
        if search_result["Answers"] == 1:
            return "%s (1 Answer)" % search_result["Title"]
        else:
            return "%s (%s Answers)" % (search_result["Title"], search_result["Answers"])


    def _stylize_question(self, title, desc, stats):
        new_title = urwid.Text(("title", u"%s" % title))
        new_stats = urwid.Text(("stats", u"%s\n" % stats))

        return [new_title, desc, new_stats]

##################################################################################

## Helper Functions ##


def confirm(question):
    """Prompts a given question and handles user input."""
    valid = {"yes": True, 'y': True, "ye": True,
             "no": False, 'n': False, '': True}
    prompt = " [Y/n] "

    while True:
        print(BOLD + CYAN + question + prompt + END)
        choice = input().lower()
        if choice in valid:
            return valid[choice]

        print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def print_help():
    """Prints usage instructions."""
    print("%sRebound, V1.1.9a1 - Made by @shobrook%s\n" % (BOLD, END))
    print("Command-line tool that automatically searches Stack Overflow and displays results in your terminal when you get a compiler error.")
    print("\n\n%sUsage:%s $ rebound %s[file_name]%s\n" % (UNDERLINE, END, YELLOW, END))
    print("\n$ python3 %stest.py%s   =>   $ rebound %stest.py%s" % (YELLOW, END, YELLOW, END))
    print("\n$ node %stest.js%s     =>   $ rebound %stest.js%s\n" % (YELLOW, END, YELLOW, END))
    print("\nIf you just want to query Stack Overflow, use the -q parameter: $ rebound -q %sWhat is an array comprehension?%s\n\n" % (YELLOW, END))


def get_question_and_answers(url):
    return "question title", urwid.Text("description"), 3, [urwid.Text("answer 1"), urwid.Text("answer 2"), urwid.Text("answer 3")]



def main():
    programming_language = get_language(sys.argv[1].lower())

    if programming_language == '': # Unknown language
            print("\n%s%s%s" % (RED, "Sorry, resolver doesn't support this file type.\n", END))
            return      


    file_path = sys.argv[1:]

    output, error = execute([programming_language] + file_path)

    error_info = inspect_error(error, programming_language)

    qry, err_hint = handle_error(error_info)

    error_message = parse_error(error, programming_language)

    query = "%s %s" % (programming_language, error_message)

    search_results = tool.search_query(query)

    answers = [result.Answer for result in search_results]

    summarized_answer = get_summarised_answer(answers)

    print(summarized_answer)

    search_results.append({
        "Title": "question number 1",
        #"Body": result.find_all("div", class_="excerpt")[0].text,
        #"Votes": int(result.find_all("span", class_="vote-count-post ")[0].find_all("strong")[0].text),
        "Answers": 1,
        "URL": "https://stackoverflow.com/questions/36788688/merge-sort-python-3/36788919"
    })

    search_results.append({
        "Title": "question number 2",
        #"Body": result.find_all("div", class_="excerpt")[0].text,
        #"Votes": int(result.find_all("span", class_="vote-count-post ")[0].find_all("strong")[0].text),
        "Answers": 1,
        "URL": "https://stackoverflow.com/questions/36788688/merge-sort-python-3/36788919"
    })

    # if confirm("\nDiplay Stack Overflow Results") :
    #     App(search_results)

       


main()