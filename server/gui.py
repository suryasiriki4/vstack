"""
showing the question and answer panel using gui with tkinter.
"""

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import sys
from .tool.tool import search_query

ques = []
answers = []

def search():
    """
    1. it gets the search query in ui
    2. calls the search_query function in tool.py and return the answer.
    """
    search_data = ent.get()

    answersStore = search_query(search_data)
    print("1\n")
    # delete current data
    ent.set(" ")
    print("1\n")
    text.delete(0.0, END)
    print("1\n")
    # insert data
    search_label["text"] = " Searching :{}".format(search_data)
    print("1\n")

    return answersStore


def enter_pressed(event):  

    answersStore = search()
    global ques
    ques = [answer[0] for answer in answersStore]
    global answers
    answers = [answer[2] for answer in answersStore]
    
    populate_list(ques, parts_list)

       



# table of questions part

def populate_list(ques, parts_list):
    i = 0
    for que in ques:
        i+=1
        parts_list.insert(END, str(i) + ". " + que)

def view(root, selected_tuple, ques, answers):

    text.delete(0.0, END)

    if len(selected_tuple) == 0:
        messagebox.showinfo("not selected", "not selected")
    else:
        text.insert(0.0, "QUESTION : \n" + ques[selected_tuple[0]] + "\n")
        text.insert(END, 39 * "*" + "\nANSER : \n" + answers[selected_tuple[0]])

"""
disigning the UI window
"""
root = Tk()
root.title("TOOL")
root.geometry("340x550")
root.configure(bg="white")

ent = StringVar()

"""
binding the text inside the UI window with the functions that call tool.py
"""

search_entry = Entry(root, width=30, font=("arial", 12),
                     bd=2, relief=RIDGE, textvariable=ent)
search_entry.bind('<Return>', enter_pressed)
search_entry.place(x=25, y=20)

search_label = Label(root, text="Searching : ", font=("arial", 12, "bold"))
search_label.place(x=25, y=70)


search_button = Button(root, text="Search", width=8, font=(
    "arial", 12, "bold"), command=search)
search_button.place(x=20, y=100)

view_button = Button(root, text="view", width=8, font=(
    "arial", 12, "bold"), command=lambda: view(root, parts_list.curselection(), ques, answers))
view_button.place(x=125, y=100)

exit_button = Button(root, text="Exit", width=8, font=(
    "arial", 12, "bold"), command=root.quit)
exit_button.place(x=230, y=100)



parts_list = Listbox(root, height=4)
parts_list.place(x=15, y=150, height=100, width=320)


text = ScrolledText(root, font=("times", 10), bd=4, relief=SUNKEN, wrap=WORD)
text.place(x=15, y=250, height=300, width=320)

# initializing the UI
root.mainloop()
