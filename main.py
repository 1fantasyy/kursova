import tkinter as tk
from views.main_menu import MainMenu
from database import connect_db

#  Основна функція програми, яка ініціалізує підключення до бази даних,
#  створює головне вікно програми та запускає головне меню
def main():
    connect_db()  # Встановлює підключення до бази даних
    root = tk.Tk()  # Створює головне вікно Tkinter
    app = MainMenu(root)  # Ініціалізує головне меню програми
    root.mainloop()  # Запускає головний цикл обробки подій Tkinter

if __name__ == "__main__":
    main()

