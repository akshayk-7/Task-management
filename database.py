import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create the tasks table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL,
                due_date TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_task(self, title, description, priority, due_date):
        """Add a new task to the database"""
        try:
            self.cursor.execute('''
                INSERT INTO tasks (title, description, priority, due_date)
                VALUES (?, ?, ?, ?)
            ''', (title, description, priority, due_date))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            return False

    def get_all_tasks(self):
        """Retrieve all tasks from the database"""
        try:
            self.cursor.execute('SELECT * FROM tasks ORDER BY due_date')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving tasks: {e}")
            return []

    def update_task(self, task_id, title, description, priority, due_date, status):
        """Update an existing task"""
        try:
            self.cursor.execute('''
                UPDATE tasks
                SET title = ?, description = ?, priority = ?, due_date = ?, status = ?
                WHERE id = ?
            ''', (title, description, priority, due_date, status, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating task: {e}")
            return False

    def delete_task(self, task_id):
        """Delete a task from the database"""
        try:
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False

    def get_task_by_id(self, task_id):
        """Retrieve a specific task by ID"""
        try:
            self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving task: {e}")
            return None

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
