import tkinter as tk
import os
from functions import get_todos, write_todos

if not os.path.exists("todos.txt"):
    with open("todos.txt", "w") as file:
        pass


class TodoApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Todo App')
        self.window.geometry('300x400')
        self.window.resizable(False, False)

        self.padding: dict = {'padx': 10, 'pady': 5}

        self.input_label = tk.Label(self.window, text='Type in a to-do: ')
        self.input_label.pack(**self.padding)

        self.input_box = tk.Entry(self.window)
        self.input_box.pack(**self.padding)

        self.list_box = tk.Listbox(self.window)
        self.list_box.pack(**self.padding)
        items = get_todos()
        for item in items:
            self.list_box.insert(tk.END, item)
        self.list_box.bind('<<ListboxSelect>>', self.show_in_input_box)

        self.add_button = tk.Button(self.window, text="Add", command=self.add_todo)
        self.add_button.pack(**self.padding)

        self.complete_button = tk.Button(self.window, text="Complete", command=self.complete)
        self.complete_button.pack(**self.padding)

        self.edit_button = tk.Button(self.window, text="Edit", command=self.edit)
        self.edit_button.pack(**self.padding)

        self.exit_button = tk.Button(self.window, text="Exit", command=self.exit)
        self.exit_button.pack(**self.padding)

    def add_todo(self):
        new_todo = self.input_box.get()
        if len(new_todo) > 0:
            todos = get_todos()
            todos.append(new_todo + "\n")
            write_todos(todos)
            self.reload_listbox()
            self.input_box.delete(0, tk.END)
        else:
            self.open_popup("Enter a todo...")

    def reload_listbox(self):
        self.list_box.delete(0, tk.END)
        items = get_todos()
        for item in items:
            self.list_box.insert(tk.END, item)

    def show_in_input_box(self, event):
        selected_index = self.list_box.curselection()
        selected_todo = self.list_box.get(selected_index)
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, selected_todo)

    def complete(self):
        index_to_complete = self.list_box.curselection()
        self.list_box.delete(index_to_complete)
        todos = self.list_box.get(0, tk.END)
        write_todos(todos)

    def edit(self):
        index_to_edit = self.list_box.curselection()
        edited_todo = self.input_box.get()
        todos = get_todos()
        todos[index_to_edit[0]] = edited_todo
        write_todos(todos)
        self.reload_listbox()

    def open_popup(self, message):
        popup = tk.Toplevel(self.window)
        popup.title(message)
        popup.geometry("100x100")

        # Example content in the popup window
        label = tk.Label(popup, text=message)
        label.pack(pady=20)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def exit(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    todoapp = TodoApp()
    todoapp.run()


