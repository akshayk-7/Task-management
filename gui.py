import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
from database import Database
import tkinter.font as tkfont

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("1000x700")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Custom.TLabelframe", background="#f0f0f0")
        self.style.configure("Custom.TLabelframe.Label", font=("Helvetica", 12, "bold"))
        self.style.configure("Custom.TButton", font=("Helvetica", 10))
        self.style.configure("Treeview", font=("Helvetica", 10))
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        
        self.db = Database()
        self.setup_gui()
        self.load_tasks()

    def setup_gui(self):
        # Create main frame with padding
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Task input frame with modern styling
        input_frame = ttk.LabelFrame(self.main_frame, text="Add New Task", padding="15", style="Custom.TLabelframe")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)

        # Title with modern font
        title_font = tkfont.Font(family="Helvetica", size=10)
        ttk.Label(input_frame, text="Title:", font=title_font).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=40, font=title_font)
        title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Description
        ttk.Label(input_frame, text="Description:", font=title_font).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        desc_entry = ttk.Entry(input_frame, textvariable=self.description_var, width=40, font=title_font)
        desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Priority with modern combobox
        ttk.Label(input_frame, text="Priority:", font=title_font).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                    values=["High", "Medium", "Low"], font=title_font)
        priority_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        priority_combo.current(1)

        # Due Date with modern calendar
        ttk.Label(input_frame, text="Due Date:", font=title_font).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.due_date = DateEntry(input_frame, width=12, background='#2c3e50',
                                foreground='white', borderwidth=2, font=title_font)
        self.due_date.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Add Task Button with modern style
        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task,
                              style="Custom.TButton")
        add_button.grid(row=4, column=1, pady=10, sticky=tk.E)

        # Task List with modern styling
        list_frame = ttk.LabelFrame(self.main_frame, text="Task List", padding="15", style="Custom.TLabelframe")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Create Treeview with modern styling
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Title", "Description", "Priority", "Due Date", "Status"),
                                show="headings", style="Treeview")
        
        # Define columns with modern styling
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")

        # Set column widths
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=150)
        self.tree.column("Description", width=300)
        self.tree.column("Priority", width=100, anchor=tk.CENTER)
        self.tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)

        # Add scrollbar with modern styling
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Action buttons with modern styling
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Create modern styled buttons
        update_btn = ttk.Button(button_frame, text="Update Task", command=self.update_task,
                              style="Custom.TButton")
        delete_btn = ttk.Button(button_frame, text="Delete Task", command=self.delete_task,
                              style="Custom.TButton")
        complete_btn = ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete,
                                style="Custom.TButton")

        # Grid buttons with proper spacing
        update_btn.grid(row=0, column=0, padx=10)
        delete_btn.grid(row=0, column=1, padx=10)
        complete_btn.grid(row=0, column=2, padx=10)

        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def load_tasks(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load tasks from database
        tasks = self.db.get_all_tasks()
        for task in tasks:
            self.tree.insert("", tk.END, values=task)

    def add_task(self):
        title = self.title_var.get().strip()
        description = self.description_var.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date.get_date().strftime("%Y-%m-%d")

        if not title:
            messagebox.showerror("Error", "Title is required!")
            return

        if self.db.add_task(title, description, priority, due_date):
            self.load_tasks()
            self.clear_inputs()
            messagebox.showinfo("Success", "Task added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add task!")

    def create_update_window(self, task):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Task")
        update_window.geometry("500x400")
        update_window.configure(padx=20, pady=20)

        # Create input fields with modern styling
        title_font = tkfont.Font(family="Helvetica", size=10)
        
        ttk.Label(update_window, text="Title:", font=title_font).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_var = tk.StringVar(value=task[1])
        ttk.Entry(update_window, textvariable=title_var, width=40, font=title_font).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(update_window, text="Description:", font=title_font).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        description_var = tk.StringVar(value=task[2])
        ttk.Entry(update_window, textvariable=description_var, width=40, font=title_font).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(update_window, text="Priority:", font=title_font).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        priority_var = tk.StringVar(value=task[3])
        priority_combo = ttk.Combobox(update_window, textvariable=priority_var, 
                                    values=["High", "Medium", "Low"], font=title_font)
        priority_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(update_window, text="Status:", font=title_font).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        status_var = tk.StringVar(value=task[5])
        status_combo = ttk.Combobox(update_window, textvariable=status_var, 
                                  values=["Pending", "Completed"], font=title_font)
        status_combo.grid(row=3, column=1, padx=5, pady=5)

        def save_update():
            if self.db.update_task(task[0], title_var.get(), description_var.get(),
                                 priority_var.get(), task[4], status_var.get()):
                self.load_tasks()
                update_window.destroy()
                messagebox.showinfo("Success", "Task updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update task!")

        # Save button with modern styling
        save_btn = ttk.Button(update_window, text="Save Changes", command=save_update,
                            style="Custom.TButton")
        save_btn.grid(row=4, column=1, pady=20, sticky=tk.E)

    def update_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to update!")
            return

        task_id = self.tree.item(selected_item[0])['values'][0]
        task = self.db.get_task_by_id(task_id)
        self.create_update_window(task)

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            task_id = self.tree.item(selected_item[0])['values'][0]
            if self.db.delete_task(task_id):
                self.load_tasks()
                messagebox.showinfo("Success", "Task deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete task!")

    def mark_complete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return

        task_id = self.tree.item(selected_item[0])['values'][0]
        task = self.db.get_task_by_id(task_id)
        
        if self.db.update_task(task_id, task[1], task[2], task[3], task[4], "Completed"):
            self.load_tasks()
            messagebox.showinfo("Success", "Task marked as complete!")
        else:
            messagebox.showerror("Error", "Failed to update task status!")

    def clear_inputs(self):
        self.title_var.set("")
        self.description_var.set("")
        self.priority_var.set("Medium")
        self.due_date.set_date(self.due_date.get_date())
