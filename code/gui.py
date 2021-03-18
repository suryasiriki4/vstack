from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys
from tool import fun

ques = []
answers = []

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


root = Tk()
root.title("TOOL")
root.geometry("320x550")
root.configure(bg="white")

ent = StringVar()

search_entry = Entry(root, width=30, font=("arial", 12),
                     bd=2, relief=RIDGE, textvariable=ent)
search_entry.bind('<Return>', enter_pressed)
search_entry.place(x=25, y=20)

search_label = Label(root, text="Searching : ", font=("arial", 12, "bold"))
search_label.place(x=25, y=70)


search_button = Button(root, text="Search", width=6, font=(
    "arial", 12, "bold"), command=search)
search_button.place(x=15, y=100)

view_button = Button(root, text="view", width=6, font=(
    "arial", 12, "bold"), command=lambda: view(root, parts_list.curselection(), ques, answers))
view_button.place(x=115, y=100)

exit_button = Button(root, text="Exit", width=6, font=(
    "arial", 12, "bold"), command=root.quit)
exit_button.place(x=215, y=100)



parts_list = Listbox(root, height=10, width=140)
parts_list.place(x=15, y=150, height=100, width=300)




text = ScrolledText(root, font=("times", 10), bd=4, relief=SUNKEN, wrap=WORD)
text.place(x=15, y=250, height=300, width=300)

root.mainloop()
