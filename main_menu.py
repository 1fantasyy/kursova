import tkinter as tk
from views.manage_trains import ManageTrains
from views.manage_wagons import ManageWagons
from views.manage_bookings import ManageBookings
from views.search import Search

    #  Головне меню програми "Залізнична каса: продаж та бронювання квитків
class MainMenu:
    def __init__(self, root): #  Ініціалізує головне вікно програми та викликає метод для створення головного вікна
        self.root = root
        self.root.title("Залізнична каса")
        self.create_main_menu()
        self.root.geometry("1420x720")

    #   Очищує вікно від дочірніх віджетів
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #  Створює головне меню з кнопками для переходу на інші вікна з різним функціоналом
    def create_main_menu(self):
        self.clear_window()
        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack(pady=20)


        tk.Button(self.main_menu, text="Управління потягами", fg="black",
                  bg="#A1F7E3", command=self.manage_trains, width=22, height=5,
                  font="Arial", bd="1", activebackground="#C7F9EE").pack(padx=25, pady=25, anchor="center")
        tk.Button(self.main_menu, text="Управління вагонами", fg="black",
                  bg="#A1F7E3", command=self.manage_wagons, width=22, height=5,
                  font="Arial", bd="1", activebackground="#C7F9EE").pack(padx=25, anchor="center", pady=25)
        tk.Button(self.main_menu, text="Управління бронюваннями", fg="black",
                  bg="#A1F7E3", command=self.manage_bookings, width=22, height=5,
                  font="Arial", bd="1", activebackground="#C7F9EE").pack(padx=25, anchor="center", pady=25)
        tk.Button(self.main_menu, text="Пошук", fg="black",
                  bg="#A1F7E3", command=self.search, width=22, height=5,
                  font="Arial", bd="1", activebackground="#C7F9EE").pack(padx=25, anchor="center", pady=25)

    #  Вікдриває вікно для управління потягами
    def manage_trains(self):
        self.clear_window()
        ManageTrains(self.root, self.create_main_menu)

    #  Відкриває вікно для управління вагонами
    def manage_wagons(self):
        self.clear_window()
        ManageWagons(self.root, self.create_main_menu)

    #  Відкриває вікно для управління бронюваннями
    def manage_bookings(self):
        self.clear_window()
        ManageBookings(self.root, self.create_main_menu)

    #  Відкриває вікно для пошуку
    def search(self):
        self.clear_window()
        Search(self.root, self.create_main_menu)





