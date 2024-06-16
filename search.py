import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from database import fetch_query
from datetime import date

    #  Клас Search створює інтерфейс для пошуку потягів за ключовим словом або бронювань за датою.
class Search:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.font = ("Times New Roman", 16, "bold")
        self.keyword_entry = None
        self.date_entry = None
        self.setup_ui()

    #  Очищує вміст головного вікна, видаляючи всі дочірні віджети.
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    #  Створює основний інтерфейс для пошуку потягів та бронювань за ключовим словом або датою.
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.TOP, anchor=tk.N, pady=20)

        tk.Button(self.button_frame, text="Пошук потягу за ключовим словом", command=self.search_trains_by_keyword, width=30, font=self.font, bg="#A1F7E3", bd=1).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Пошук бронювання за датою", command=self.search_bookings_by_date, width=30, font=self.font, bg="#A1F7E3", bd=1).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Назад", command=self.back_callback, width=30, font=self.font, bg="#A1F7E3", bd=1).pack(side=tk.LEFT, padx=5, pady=5)

        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    #  Відображає інтерфейс для пошуку потягів за ключовим словом
    def search_trains_by_keyword(self):
        self.clear_content()

        tk.Label(self.content_frame, text="Введіть ключове слово (назва, пункт відправлення/прибуття):", font=self.font).pack(pady=10)
        self.keyword_entry = tk.Entry(self.content_frame, font=self.font)
        self.keyword_entry.pack(pady=10)

        tk.Button(self.content_frame, text="Знайти", bg="#A1F7E3", command=self.perform_search_trains_by_keyword, width=20, font=self.font).pack(pady=10)

    #  Виконує пошук потягів за ключовим словом у базі даних і відображає результати
    def perform_search_trains_by_keyword(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showerror("Помилка", "Введіть ключове слово.")
            return

        query = "SELECT * FROM Train WHERE LOWER(origin) LIKE LOWER(?) OR LOWER(destination) LIKE LOWER(?) OR LOWER(name) LIKE LOWER(?)"
        params = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        results = fetch_query(query, params)

        if results:
            self.clear_content()
            for result in results:
                tk.Label(self.content_frame, text=f"ID Потягу: {result[0]}, Назва: {result[3]}, Звідки: {result[1]}, Куди: {result[2]}, Дата: {result[4]}", font=self.font).pack(pady=5)
        else:
            self.keyword_entry.delete(0, tk.END)
            messagebox.showinfo("Результат", "Нічого не знайдено. Спробуйте ще раз.")

    #  Відображає інтерфейс для пошуку бронювань за датою
    def search_bookings_by_date(self):
        self.clear_content()

        tk.Label(self.content_frame, text="Введіть дату бронювання:", font=self.font).pack(pady=10)
        self.date_entry = DateEntry(self.content_frame, date_pattern='dd.mm.yyyy', font=self.font)
        self.date_entry.pack(pady=10)

        tk.Button(self.content_frame, text="Знайти", bg="#A1F7E3", command=self.perform_search_bookings_by_date, width=20, font=self.font).pack(pady=10)

    #  Виконує пошук бронювань за введеною користувачем датою і відображає результати.
    def perform_search_bookings_by_date(self):
        booking_date = self.date_entry.get()
        if not booking_date:
            messagebox.showerror("Помилка", "Введіть дату.")
            return

        query = '''
        SELECT Booking.id, Booking.train_id, Booking.wagon_id, Booking.seat_number, Train.name, Train.origin, Train.destination, Train.date
        FROM Booking 
        JOIN Train ON Booking.train_id = Train.id 
        WHERE Train.date = ?
        '''
        results = fetch_query(query, (booking_date,))

        if results:
            self.clear_content()
            for result in results:
                booking_info = f"Звідки: {result[5]}, Куди: {result[6]}, Назва потягу: {result[4]}, Дата: {result[7]}, Номер вагону: {result[2]}, Місце бронювання: {result[3]}, ID Потягу: {result[1]}"
                tk.Label(self.content_frame, text=booking_info, font=self.font).pack(pady=5)
        else:
            self.date_entry.set_date(date.today())
            messagebox.showinfo("Результат", "Немає бронювань на вказану дату.")

















