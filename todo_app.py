import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.root.geometry("400x400")

        # Initialize SQLite database
        self.conn = sqlite3.connect('todo.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
        self.conn.commit()

        # GUI Elements
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=40, height=15)
        self.task_listbox.pack(pady=10)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        # Load tasks from database
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.conn.commit()
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            selected_task = self.task_listbox.get(selected_task_index)
            self.c.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
            self.conn.commit()
            self.task_listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def load_tasks(self):
        self.c.execute("SELECT task FROM tasks")
        tasks = self.c.fetchall()
        for task in tasks:
            self.task_listbox.insert(tk.END, task[0])

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()