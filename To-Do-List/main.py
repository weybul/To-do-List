from tkinter import *
from tkinter import messagebox

root = Tk()

root.geometry("300x450")
root.maxsize(300,450)
root.minsize(300,450)
root.title("Just Do It")

# creatin an entry widget
entry = Entry(root, bd=6, bg="green", font=("Ariel", 12, "bold italic underline"), fg="yellow")
entry.pack(fill=X)

# frame for listbox widget
listbox_frame = Frame(root, relief="groove", bd=11, bg="green")
listbox_frame.pack(fill=BOTH, expand=True)

# listbox
listbox = Listbox(listbox_frame, bd=4, bg="green", fg="yellow", font=("helvetic", 14, "bold italic"), selectbackground="green")
listbox.pack(fill=BOTH, expand=True, padx=3, pady=3)

# frame for scrollbar
scrb_frame = Frame(listbox, width=6, relief="ridge", bd=3, bg="darkgreen")
scrb_frame.pack(side=RIGHT, fill=Y)

# addin scrollbar
scrb = Scrollbar(scrb_frame)
scrb.pack(side=RIGHT, fill=Y)

# configure scrollbar to control the listbox
listbox.config(yscrollcommand=scrb.set)
scrb.config(command=listbox.yview)

tasks = [] #stores the tasks
check_buttons = [] #stores excess check buttons
del_buttons = [] #srores excess delete buttons

def load_tasks(): #loads the saved tasks from tasks.txt upon starting the program
    global tasks #declaring tasks as a global variable
    try:
        with open("tasks.txt", "r") as f:
            tasks = []
            for line in f.readlines():
                lines =  line.strip().split(",")
                completed_tasks = lines[1].lower() == "true" #
                tasks.append({"task":lines[0], "completed":completed_tasks})
    except:
        tasks = []

# with the listbox configurations out the way we can now implement the logic behind our to do list
# lets start by creating a function 1st of all that accepts the tasks entered by the user
def add_task(event=None):
    task = entry.get() #retrieves the input from the entry widget
    tasks.append({"task":task, "completed":False}) #turns task's text into a dict key and the boolean to their value
    update_listbox()
    save_tasks()
    entry.delete(0, END)

def update_listbox(): #updates the listbox visually to represent the tasks bein entered
    listbox.delete(0, END) #makes sure the previously entered tasks arent repeated with the new one
    for index, task in enumerate(tasks):
        button_frame = Frame(listbox, bg="green") #keeps del,check buttons in the same line as tasks
        button_frame.pack(anchor=E, pady=2)
        task_text = task["task"]
        if task["completed"]:
            task_text += "  ✔️" #marks a completed task with the unicode character
        listbox.insert(END, task_text)

        # update or create check buttons
        if index < len(check_buttons): #if a task's range is within th existing check buttons
            check_button = check_buttons[index] #retrieve the corresponding button for that task
            check_button.config(command=lambda i=index:toggle_task(i))
        else:
            # create check button
            check_button = Button(button_frame, text="✔️", bd=3, bg="green", fg="yellow", font=("helvetic", 6, "bold"), command=lambda i=index:toggle_task(i))
            check_button.pack(side=RIGHT, padx=2)
            check_buttons.append(check_button)

        # update or create new delete_buttons
        if index < len(del_buttons):
            del_button = del_buttons[index]
            del_button.config(command=lambda i=index:confirm_deletion(i))
        else:
            del_button = Button(button_frame, text="❌", bd=3, bg="black", fg="red", font=("Ariel", 6), command=lambda i=index:confirm_deletion(i))
            del_button.pack(side=LEFT, padx=2)
            del_buttons.append(del_button)

    # remove extra buttons
    for check_button in check_buttons[len(tasks):]: #any buttons that r after the len of the tasks
        check_button.destroy() #remove them
    del check_buttons[len(tasks):] #also remove them from the check_buttons list

    # same for the del_buttons
    for del_button in del_buttons[len(tasks):]:
        del_button.destroy()
    del del_buttons[len(tasks):]

# a func that will save the tasks to a txt file for persistence over sessions
def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task["task"] + "," + str(task["completed"]) + "\n") #saves tasks(keys) and their values(as string)

# marks tasks as complete
def toggle_task(index):
    tasks[index]["completed"] = not tasks[index]["completed"] #flips the state of a task from comp to not from not to comp
    update_listbox() 
    save_tasks()

# prompts user with a confirmation message
def confirm_deletion(index):
    confirm = messagebox.askyesno("Confirm Deletion", "do u really want to delete this task?")
    if confirm:
        delete_task(index)

# responsible for deleting a task
def delete_task(index):
    del tasks[index]
    update_listbox()
    save_tasks()

# binds the return key to entry widget
entry.bind("<Return>", add_task)

load_tasks()
update_listbox()

root.mainloop()