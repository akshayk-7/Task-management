import tkinter as tk
from ttkthemes import ThemedTk
from gui import TaskManagerGUI

def main():
    # Create themed root window with a modern theme
    root = ThemedTk(theme="arc")
    
    # Set window icon and title
    root.title("Task Manager")
    
    # Configure window size and position
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Create and run the application
    app = TaskManagerGUI(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()

