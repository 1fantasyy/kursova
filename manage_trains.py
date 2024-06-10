import tkinter as tk
from tkinter import messagebox
from database import execute_query, fetch_query

class ManageTrains:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.manage_trains_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def manage_trains_menu(self):
        self.clear_window()
        self.train_menu = tk.Frame(self.root)
        self.train_menu.pack(pady=20)

        tk.Button(self.train_menu, text="Add Train", command=self.add_train, width=20).pack(pady=10)
        tk.Button(self.train_menu, text="View All Trains", command=self.view_trains, width=20).pack(pady=10)
        tk.Button(self.train_menu, text="Back", command=self.back_callback, width=20).pack(pady=10)

    def add_train(self):
        self.clear_window()
        self.add_train_menu = tk.Frame(self.root)
        self.add_train_menu.pack(pady=20)

        tk.Label(self.add_train_menu, text="Origin:").pack()
        self.origin_entry = tk.Entry(self.add_train_menu)
        self.origin_entry.pack()

        tk.Label(self.add_train_menu, text="Destination:").pack()
        self.destination_entry = tk.Entry(self.add_train_menu)
        self.destination_entry.pack()

        tk.Label(self.add_train_menu, text="Name:").pack()
        self.name_entry = tk.Entry(self.add_train_menu)
        self.name_entry.pack()

        tk.Label(self.add_train_menu, text="Date:").pack()
        self.date_entry = tk.Entry(self.add_train_menu)
        self.date_entry.pack()

        tk.Button(self.add_train_menu, text="Add Train", command=self.save_train, width=20).pack(pady=10)
        tk.Button(self.add_train_menu, text="Back", command=self.manage_trains_menu, width=20).pack(pady=10)

    def save_train(self):
        origin = self.origin_entry.get()
        destination = self.destination_entry.get()
        name = self.name_entry.get()
        date = self.date_entry.get()

        if origin and destination and name and date:
            execute_query('INSERT INTO Train (origin, destination, name, date) VALUES (?, ?, ?, ?)',
                          (origin, destination, name, date))
            messagebox.showinfo("Success", "Train added successfully!")
            self.origin_entry.delete(0, tk.END)
            self.destination_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required!")

    def view_trains(self):
        self.clear_window()
        self.view_trains_menu = tk.Frame(self.root)
        self.view_trains_menu.pack(pady=20)

        trains = fetch_query('SELECT * FROM Train')

        for train in trains:
            wagons = fetch_query('SELECT id, number, seats FROM Wagon WHERE train_id = ?', (train[0],))
            wagon_info = []
            for wagon in wagons:
                bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
                booked_seats = [booking[0] for booking in bookings]
                available_seats = wagon[2] - len(booked_seats)
                wagon_info.append(
                    f"Wagon {wagon[1]}: {', '.join(map(str, booked_seats)) if booked_seats else 'All seats available'}. Available: {available_seats}")

            train_info = f"Train ID: {train[0]}, Name: {train[3]}, From: {train[1]}, To: {train[2]}, Date: {train[4]}, Wagons: {', '.join(wagon_info)}"
            tk.Label(self.view_trains_menu, text=train_info).pack(pady=5)

        tk.Button(self.view_trains_menu, text="Back", command=self.manage_trains_menu, width=20).pack(pady=10)

    def delete_train(self, train_id):
        bookings_count = fetch_query('SELECT COUNT(*) FROM Booking WHERE train_id = ?', (train_id,))[0][0]

        if bookings_count > 0:
            messagebox.showerror("Error", "Cannot delete train with bookings!")
        else:
            execute_query('DELETE FROM Train WHERE id = ?', (train_id,))
            messagebox.showinfo("Success", "Train deleted successfully!")
            self.view_trains()
