import tkinter as tk
from tkinter import messagebox
from database import fetch_query

class Search:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.search_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def search_menu(self):
        self.clear_window()
        self.search_menu_frame = tk.Frame(self.root)
        self.search_menu_frame.pack(pady=20)

        tk.Button(self.search_menu_frame, text="Search Trains by Keyword", command=self.search_trains_by_keyword, width=30).pack(pady=10)
        tk.Button(self.search_menu_frame, text="Search Bookings by Date", command=self.search_bookings_by_date, width=30).pack(pady=10)
        tk.Button(self.search_menu_frame, text="Back", command=self.back_callback, width=30).pack(pady=10)

    def search_trains_by_keyword(self):
        self.clear_window()
        self.search_trains_frame = tk.Frame(self.root)
        self.search_trains_frame.pack(pady=20)

        tk.Label(self.search_trains_frame, text="Enter keyword:").pack()
        self.keyword_entry = tk.Entry(self.search_trains_frame)
        self.keyword_entry.pack()

        tk.Button(self.search_trains_frame, text="Search", command=self.perform_search_trains_by_keyword, width=20).pack(pady=10)
        tk.Button(self.search_trains_frame, text="Back", command=self.search_menu, width=20).pack(pady=10)

    def perform_search_trains_by_keyword(self):
        keyword = self.keyword_entry.get()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword.")
            return

        query = "SELECT * FROM Train WHERE origin LIKE ? OR destination LIKE ? OR name LIKE ?"
        params = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        results = fetch_query(query, params)

        self.clear_window()
        self.search_results_frame = tk.Frame(self.root)
        self.search_results_frame.pack(pady=20)

        for result in results:
            tk.Label(self.search_results_frame, text=f"Train ID: {result[0]}, Name: {result[3]}, From: {result[1]}, To: {result[2]}, Date: {result[4]}").pack(pady=5)

        tk.Button(self.search_results_frame, text="Back", command=self.search_menu, width=20).pack(pady=10)

    def search_bookings_by_date(self):
        self.clear_window()
        self.search_bookings_frame = tk.Frame(self.root)
        self.search_bookings_frame.pack(pady=20)

        tk.Label(self.search_bookings_frame, text="Enter date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.search_bookings_frame)
        self.date_entry.pack()

        tk.Button(self.search_bookings_frame, text="Search", command=self.perform_search_bookings_by_date, width=20).pack(pady=10)
        tk.Button(self.search_bookings_frame, text="Back", command=self.search_menu, width=20).pack(pady=10)

    def perform_search_bookings_by_date(self):
        booking_date = self.date_entry.get()
        if not booking_date:
            messagebox.showerror("Error", "Please enter a date.")
            return

        query = '''
        SELECT Booking.id, Booking.train_id, Booking.wagon_id, Booking.seat_number, Train.date 
        FROM Booking 
        JOIN Train ON Booking.train_id = Train.id 
        WHERE Train.date = ?
        '''
        results = fetch_query(query, (booking_date,))

        self.clear_window()
        self.search_results_frame = tk.Frame(self.root)
        self.search_results_frame.pack(pady=20)

        for result in results:
            tk.Label(self.search_results_frame, text=f"Booking ID: {result[0]}, Train ID: {result[1]}, Wagon ID: {result[2]}, Seat Number: {result[3]}, Date: {result[4]}").pack(pady=5)

        tk.Button(self.search_results_frame, text="Back", command=self.search_menu, width=20).pack(pady=10)

