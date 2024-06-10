import tkinter as tk
from views.manage_trains import ManageTrains
from views.manage_wagons import ManageWagons
from views.manage_bookings import ManageBookings
from views.search import Search

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Booking System")
        self.create_main_menu()
        self.root.geometry("1820x1020")


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()
        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack(pady=20)


        tk.Button(self.main_menu, text="Manage Trains", command=self.manage_trains, width=20).pack(pady=10)
        tk.Button(self.main_menu, text="Manage Wagons", command=self.manage_wagons, width=20).pack(pady=10)
        tk.Button(self.main_menu, text="Manage Bookings", command=self.manage_bookings, width=20).pack(pady=10)
        tk.Button(self.main_menu, text="Search", command=self.search, width=20).pack(pady=10)

    def manage_trains(self):
        self.clear_window()
        ManageTrains(self.root, self.create_main_menu)

    def manage_wagons(self):
        self.clear_window()
        ManageWagons(self.root, self.create_main_menu)

    def manage_bookings(self):
        self.clear_window()
        ManageBookings(self.root, self.create_main_menu)

    def search(self):
        self.clear_window()
        Search(self.root, self.create_main_menu)


