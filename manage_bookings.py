import tkinter as tk
from tkinter import messagebox
from database import fetch_query, execute_query


class ManageBookings:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.manage_bookings_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def manage_bookings_menu(self):
        self.clear_window()
        self.booking_menu = tk.Frame(self.root)
        self.booking_menu.pack(pady=20)

        tk.Button(self.booking_menu, text="Add Booking", command=self.add_booking, width=20).pack(pady=10)
        tk.Button(self.booking_menu, text="View All Bookings", command=self.view_bookings, width=20).pack(pady=10)
        tk.Button(self.booking_menu, text="Cancel Booking", command=self.cancel_booking, width=20).pack(pady=10)
        tk.Button(self.booking_menu, text="Modify Booking", command=self.modify_booking, width=20).pack(pady=10)
        tk.Button(self.booking_menu, text="View All Trains", command=self.view_trains, width=20).pack(pady=10)
        tk.Button(self.booking_menu, text="Back", command=self.back_callback, width=20).pack(pady=10)

    def view_trains(self):
        self.clear_window()
        self.view_trains_menu = tk.Frame(self.root)
        self.view_trains_menu.pack(pady=20)

        trains = fetch_query('SELECT * FROM Train')

        for train in trains:
            wagons = fetch_query('SELECT id, number FROM Wagon WHERE train_id = ?', (train[0],))
            wagon_info = []
            for wagon in wagons:
                bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
                booked_seats = [booking[0] for booking in bookings]
                wagon_info.append(
                    f"Wagon {wagon[1]}: {', '.join(map(str, booked_seats)) if booked_seats else 'All seats available'}")

            train_info = f"Train ID: {train[0]}, Name: {train[3]}, From: {train[1]}, To: {train[2]}, Date: {train[4]}, Wagons: {', '.join(wagon_info)}"
            tk.Label(self.view_trains_menu, text=train_info).pack(pady=5)

        tk.Button(self.view_trains_menu, text="Back", command=self.manage_bookings_menu, width=20).pack(pady=10)

    def add_booking(self):
        self.clear_window()
        self.add_booking_menu = tk.Frame(self.root)
        self.add_booking_menu.pack(pady=20)

        tk.Label(self.add_booking_menu, text="Select Train:").pack()
        self.train_var = tk.StringVar(self.add_booking_menu)
        trains = fetch_query('SELECT id, name FROM Train')
        self.train_var.set("Select a train")
        train_options = [f"{train[0]} - {train[1]}" for train in trains]
        self.train_menu = tk.OptionMenu(self.add_booking_menu, self.train_var, *train_options)
        self.train_menu.pack()

        tk.Label(self.add_booking_menu, text="Select Wagon:").pack()
        self.wagon_var = tk.StringVar(self.add_booking_menu)
        self.wagon_menu = tk.OptionMenu(self.add_booking_menu, self.wagon_var, "")
        self.wagon_menu.pack()

        self.train_var.trace('w', self.update_wagon_menu)

        tk.Label(self.add_booking_menu, text="Seat Number:").pack()
        self.seat_number_entry = tk.Entry(self.add_booking_menu)
        self.seat_number_entry.pack()

        tk.Button(self.add_booking_menu, text="Add Booking", command=self.save_booking, width=20).pack(pady=10)
        tk.Button(self.add_booking_menu, text="Back", command=self.manage_bookings_menu, width=20).pack(pady=10)

    def update_wagon_menu(self, *args):
        train_id = self.train_var.get().split(" - ")[0]
        wagons = fetch_query('SELECT id, number FROM Wagon WHERE train_id = ?', (train_id,))
        self.wagon_var.set("")
        menu = self.wagon_menu["menu"]
        menu.delete(0, "end")
        for wagon in wagons:
            bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
            booked_seats = [booking[0] for booking in bookings]
            menu.add_command(label=f"{wagon[0]} - {wagon[1]} (Booked seats: {', '.join(map(str, booked_seats))})",
                             command=lambda value=f"{wagon[0]} - {wagon[1]}": self.wagon_var.set(value))

    def save_booking(self):
        train_id = self.train_var.get().split(" - ")[0]
        wagon_id = self.wagon_var.get().split(" - ")[0]
        seat_number = self.seat_number_entry.get()

        if train_id and wagon_id and seat_number:
            execute_query('INSERT INTO Booking (train_id, wagon_id, seat_number) VALUES (?, ?, ?)',
                          (train_id, wagon_id, seat_number))
            messagebox.showinfo("Success", "Booking added successfully!")
            self.seat_number_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required!")

    def view_bookings(self):
        self.clear_window()
        self.view_bookings_menu = tk.Frame(self.root)
        self.view_bookings_menu.pack(pady=20)

        bookings = fetch_query('SELECT * FROM Booking')

        for booking in bookings:
            booking_info = f"Booking ID: {booking[0]}, Train ID: {booking[1]}, Wagon ID: {booking[2]}, Seat Number: {booking[3]}"
            tk.Label(self.view_bookings_menu, text=booking_info).pack(pady=5)

        tk.Button(self.view_bookings_menu, text="Back", command=self.manage_bookings_menu, width=20).pack(pady=10)

    def cancel_booking(self):
        self.clear_window()
        self.cancel_booking_menu = tk.Frame(self.root)
        self.cancel_booking_menu.pack(pady=20)

        tk.Label(self.cancel_booking_menu, text="Enter Booking ID to cancel:").pack()
        self.booking_id_entry = tk.Entry(self.cancel_booking_menu)
        self.booking_id_entry.pack()

        tk.Button(self.cancel_booking_menu, text="Cancel Booking", command=self.delete_booking, width=20).pack(pady=10)
        tk.Button(self.cancel_booking_menu, text="Back", command=self.manage_bookings_menu, width=20).pack(pady=10)

    def delete_booking(self):
        booking_id = self.booking_id_entry.get()

        if booking_id:
            execute_query('DELETE FROM Booking WHERE id = ?', (booking_id,))
            messagebox.showinfo("Success", "Booking cancelled successfully!")
            self.booking_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a Booking ID.")

    def modify_booking(self):
        self.clear_window()
        self.modify_booking_menu = tk.Frame(self.root)
        self.modify_booking_menu.pack(pady=20)

        tk.Label(self.modify_booking_menu, text="Enter Booking ID to modify:").pack()
        self.booking_id_entry = tk.Entry(self.modify_booking_menu)
        self.booking_id_entry.pack()

        tk.Label(self.modify_booking_menu, text="New Train:").pack()
        self.new_train_var = tk.StringVar(self.modify_booking_menu)
        trains = fetch_query('SELECT id, name FROM Train')
        self.new_train_var.set("Select a train")
        train_options = [f"{train[0]} - {train[1]}" for train in trains]
        self.new_train_menu = tk.OptionMenu(self.modify_booking_menu, self.new_train_var, *train_options)
        self.new_train_menu.pack()

        tk.Label(self.modify_booking_menu, text="New Wagon:").pack()
        self.new_wagon_var = tk.StringVar(self.modify_booking_menu)
        self.new_wagon_menu = tk.OptionMenu(self.modify_booking_menu, self.new_wagon_var, "")
        self.new_wagon_menu.pack()

        self.new_train_var.trace('w', self.update_new_wagon_menu)

        tk.Label(self.modify_booking_menu, text="New Seat Number:").pack()
        self.new_seat_number_entry = tk.Entry(self.modify_booking_menu)
        self.new_seat_number_entry.pack()

        tk.Button(self.modify_booking_menu, text="Modify Booking", command=self.update_booking, width=20).pack(pady=10)
        tk.Button(self.modify_booking_menu, text="Back", command=self.manage_bookings_menu, width=20).pack(pady=10)

    def update_new_wagon_menu(self, *args):
        train_id = self.new_train_var.get().split(" - ")[0]
        wagons = fetch_query('SELECT id, number FROM Wagon WHERE train_id = ?', (train_id,))
        self.new_wagon_var.set("")
        menu = self.new_wagon_menu["menu"]
        menu.delete(0, "end")
        for wagon in wagons:
            bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
            booked_seats = [booking[0] for booking in bookings]
            menu.add_command(label=f"{wagon[0]} - {wagon[1]} (Booked seats: {', '.join(map(str, booked_seats))})",
                             command=lambda value=f"{wagon[0]} - {wagon[1]}": self.new_wagon_var.set(value))

    def update_booking(self):
        booking_id = self.booking_id_entry.get()
        new_train_id = self.new_train_var.get().split(" - ")[0]
        new_wagon_id = self.new_wagon_var.get().split(" - ")[0]
        new_seat_number = self.new_seat_number_entry.get()

        if booking_id and new_train_id and new_wagon_id and new_seat_number:
            execute_query('UPDATE Booking SET train_id = ?, wagon_id = ?, seat_number = ? WHERE id = ?',
                          (new_train_id, new_wagon_id, new_seat_number, booking_id))
            messagebox.showinfo("Success", "Booking modified successfully!")
            self.booking_id_entry.delete(0, tk.END)
            self.new_seat_number_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required!")


