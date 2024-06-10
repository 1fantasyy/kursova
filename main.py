import tkinter as tk
from views.main_menu import MainMenu
from database import connect_db

def main():
    connect_db()
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
