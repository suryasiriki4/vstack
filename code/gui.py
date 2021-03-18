from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys
from tool import fun


def search():

    search_data = ent.get()

    answersStore = fun(search_data)
    print("1\n")
    # delete current data
    ent.set(" ")
    print("1\n")
    text.delete(0.0, END)
    print("1\n")
    # insert data
    search_label["text"] = " Searching :{}".format(search_data)
    print("1\n")
    text.insert(0.0, answersStore[0][0])
    print("1\n")


def enter_pressed(event):
    search()


root = Tk()
root.title("TOOL")
root.geometry("320x450")
root.configure(bg="white")

ent = StringVar()

search_entry = Entry(root, width=30, font=("arial", 12),
                     bd=2, relief=RIDGE, textvariable=ent)
search_entry.bind('<Return>', enter_pressed)
search_entry.place(x=25, y=20)

search_label = Label(root, text="Searching : ", font=("arial", 12, "bold"))
search_label.place(x=25, y=70)

text = ScrolledText(root, font=("times", 10), bd=4, relief=SUNKEN, wrap=WORD)
text.place(x=15, y=100, height=300, width=300)


search_button = Button(root, text="Search", width=6, font=(
    "arial", 12, "bold"), command=search)
search_button.place(x=15, y=400)

clear_button = Button(root, text="Clear", width=6, font=(
    "arial", 12, "bold"), command=lambda: text.delete(0.0, END))
clear_button.place(x=115, y=400)

exit_button = Button(root, text="Exit", width=6, font=(
    "arial", 12, "bold"), command=root.quit)
exit_button.place(x=215, y=400)

root.mainloop()
