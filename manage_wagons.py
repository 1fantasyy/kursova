import tkinter as tk
from tkinter import messagebox
from database import execute_query, fetch_query

class ManageWagons:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.manage_wagons_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def manage_wagons_menu(self):
        self.clear_window()
        self.wagon_menu = tk.Frame(self.root)
        self.wagon_menu.pack(pady=20)

        tk.Button(self.wagon_menu, text="Add Wagon", command=self.add_wagon, width=20).pack(pady=10)
        tk.Button(self.wagon_menu, text="View All Wagons", command=self.view_wagons, width=20).pack(pady=10)
        tk.Button(self.wagon_menu, text="Back", command=self.back_callback, width=20).pack(pady=10)

    def add_wagon(self):
        self.clear_window()
        self.add_wagon_menu = tk.Frame(self.root)
        self.add_wagon_menu.pack(pady=20)

        tk.Label(self.add_wagon_menu, text="Select Train:").pack()
        self.train_var = tk.StringVar(self.add_wagon_menu)
        trains = fetch_query('SELECT id, name FROM Train')
        self.train_var.set("Select a train")
        train_options = [f"{train[0]} - {train[1]}" for train in trains]
        self.train_menu = tk.OptionMenu(self.add_wagon_menu, self.train_var, *train_options)
        self.train_menu.pack()

        tk.Label(self.add_wagon_menu, text="Wagon Number:").pack()
        self.wagon_number_entry = tk.Entry(self.add_wagon_menu)
        self.wagon_number_entry.pack()

        tk.Label(self.add_wagon_menu, text="Seats:").pack()
        self.seats_entry = tk.Entry(self.add_wagon_menu)
        self.seats_entry.pack()

        tk.Button(self.add_wagon_menu, text="Add Wagon", command=self.save_wagon, width=20).pack(pady=10)
        tk.Button(self.add_wagon_menu, text="Back", command=self.manage_wagons_menu, width=20).pack(pady=10)

    def save_wagon(self):
        train_id = self.train_var.get().split(" - ")[0]
        number = self.wagon_number_entry.get()
        seats = self.seats_entry.get()

        if train_id and number and seats:
            execute_query('INSERT INTO Wagon (train_id, number, seats) VALUES (?, ?, ?)',
                          (train_id, number, seats))
            messagebox.showinfo("Success", "Wagon added successfully!")
            self.wagon_number_entry.delete(0, tk.END)
            self.seats_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required!")

    def view_wagons(self):
        self.clear_window()
        self.view_wagons_menu = tk.Frame(self.root)
        self.view_wagons_menu.pack(pady=20)

        wagons = fetch_query('SELECT * FROM Wagon')

        for wagon in wagons:
            bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
            booked_seats = [booking[0] for booking in bookings]
            try:
                available_seats = int(wagon[2]) - len(booked_seats)
            except ValueError:
                # Якщо кількість місць не може бути перетворена у ціле число, встановлюємо доступні місця як невідомі
                available_seats = "Unknown"
            wagon_info = f"Wagon ID: {wagon[0]}, Number: {wagon[1]}, Train ID: {wagon[3]}, Booked seats: {', '.join(map(str, booked_seats)) if booked_seats else 'None'}. Available seats: {available_seats}"
            tk.Label(self.view_wagons_menu, text=wagon_info).pack(pady=5)

        tk.Button(self.view_wagons_menu, text="Back", command=self.manage_wagons_menu, width=20).pack(pady=10)
