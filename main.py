import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from tkcalendar import Calendar

# Database setup
CNC = sqlite3.connect('NoteCal.db')
c = CNC.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS notes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 task TEXT NOT NULL,
                 date TEXT NOT NULL,
                 time TEXT NOT NULL,
                 description TEXT
             )''')

CNC.commit()

class NCalApp:
    def __init__(self, root):
        self.root = root
        self.root.title('NCalApp')
        self.root.geometry('1440x900')

        self.tabs = ttk.Notebook(root)
        self.notesTab = ttk.Frame(self.tabs)
        self.calTab = ttk.Frame(self.tabs)

        self.tabs.add(self.notesTab, text='🗒 Notes')
        self.tabs.add(self.calTab, text='📅 Calendar')
        self.tabs.pack(expand=1, fill='both')

        # Notes Section
        self.notesList = tk.Listbox(self.notesTab, font=('Roboto', 20))
        self.notesList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notesList.bind("<Double-Button-1>", self.view_note)
        self.load_notes()
        self.notesFrame = tk.Frame(self.notesTab)
        self.notesFrame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.add_note = tk.Button(self.notesFrame, text="📥 Add Note", command=self.add_note)
        self.add_note.pack(fill=tk.X)

        self.edit_note = tk.Button(self.notesFrame, text="📎 Edit Note", command=self.edit_note)
        self.edit_note.pack(fill=tk.X)

        self.delete_note = tk.Button(self.notesFrame, text="📤 Delete Note", command=self.delete_note)
        self.delete_note.pack(fill=tk.X)

        # Calendar Section
        self.calendarFrame = tk.Frame(self.calTab)
        self.calendarFrame.pack(side=tk.LEFT, padx=10, pady=10)
        self.calendar = Calendar(self.calendarFrame, selectmode='day', date_pattern='y-mm-dd',
                                 font=('Roboto', 15), background='white', foreground='black')
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.load_cal_task)

        self.taskFrame = tk.Frame(self.calTab)
        self.taskFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.taskList = tk.Listbox(self.taskFrame, font=('Roboto', 20))
        self.taskList.pack(fill=tk.BOTH, expand=True)

        self.task_button = tk.Frame(self.taskFrame)
        self.task_button.pack(fill=tk.X, pady=5)

        self.add_task = tk.Button(self.task_button, text="📥 Add Task", command=self.add_task)
        self.add_task.pack(side=tk.LEFT, padx=5)

        self.delete_task = tk.Button(self.task_button, text="📤 Delete Task", command=self.delete_task)
        self.delete_task.pack(side=tk.LEFT, padx=5)

        self.view_task = tk.Button(self.task_button, text="👀 View Task", command=self.task_view)
        self.view_task.pack(side=tk.LEFT, padx=5)

        self.detailsFrame = tk.Frame(self.calTab, relief=tk.RAISED, borderwidth=1)
        self.detailsFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.details_label = tk.Label(self.detailsFrame, text="📝 Task Details", font=('Roboto', 20, 'bold'))
        self.details_label.pack(anchor='nw', padx=10, pady=5)

        self.details_text = tk.Text(self.detailsFrame, font=('Roboto', 20), wrap=tk.WORD, state=tk.DISABLED)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


    def load_notes(self):
        self.notesList.delete(0, tk.END)
        c.execute("SELECT id, title FROM notes")
        for note in c.fetchall():
            self.notesList.insert(tk.END, f"{note[0]}: {note[1]}")

    def add_note(self):
        title = simpledialog.askstring("Title", "Enter the title of the note:")
        content = simpledialog.askstring("Content", "Enter the content of the note:")
        if title and content:
            c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            CNC.commit()
            self.load_notes()

    def edit_note(self):
        selected = self.notesList.curselection()
        if selected:
            note_id = int(self.notesList.get(selected[0]).split(":")[0])
            title = simpledialog.askstring("Title", "Edit the title of the note:")
            content = simpledialog.askstring("Content", "Edit the content of the note:")
            if title and content:
                c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
                CNC.commit()
                self.load_notes()

    def delete_note(self):
        selected = self.notesList.curselection()
        if selected:
            note_id = int(self.notesList.get(selected[0]).split(":")[0])
            c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            CNC.commit()
            self.load_notes()

    def view_note(self, event):
        selected = self.notesList.curselection()
        if selected:
            note_id = int(self.notesList.get(selected[0]).split(":")[0])
            c.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
            note = c.fetchone()
            messagebox.showinfo(note[0], note[1])

    def load_tasks(self):
        self.taskList.delete(0, tk.END)
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete('1.0', tk.END)
        self.details_text.config(state=tk.DISABLED)
        selected_date = self.calendar.get_date()
        c.execute("SELECT id, task, time FROM tasks WHERE date = ?", (selected_date,))
        for task in c.fetchall():
            self.taskList.insert(tk.END, f"{task[0]}: {task[1]} at {task[2]}")

    def load_cal_task(self, event):
        self.load_tasks()

    def add_task(self):
        task = simpledialog.askstring("Task", "Enter the task title:")
        description = simpledialog.askstring("Description", "Enter the task description:")
        time = simpledialog.askstring("Time", "Enter the time (e.g., 14:00):")
        date = self.calendar.get_date()
        if task and time:
            c.execute("INSERT INTO tasks (task, date, time, description) VALUES (?, ?, ?, ?)",
                      (task, date, time, description))
            CNC.commit()
            self.load_tasks()

    def delete_task(self):
        selected = self.taskList.curselection()
        if selected:
            task_id = int(self.taskList.get(selected[0]).split(":")[0])
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            CNC.commit()
            self.load_tasks()

    def task_view(self):
        selected = self.taskList.curselection()
        if selected:
            task_id = int(self.taskList.get(selected[0]).split(":")[0])
            c.execute("SELECT task, time, description FROM tasks WHERE id = ?", (task_id,))
            task = c.fetchone()
            task_info = f"Task: {task[0]}\nTime: {task[1]}\nDescription: {task[2]}"
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete('1.0', tk.END)
            self.details_text.insert(tk.END, task_info)
            self.details_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = NCalApp(root)
    root.mainloop()

    CNC.close()
