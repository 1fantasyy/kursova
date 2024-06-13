import tkinter as tk
from tkinter import messagebox
from database import execute_query, fetch_query

#  Клас для управління потягами у програмі "Залізнична каса"
class ManageTrains:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.manage_trains_menu()

#  Очищає вікно від дочірніх віджетів
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

#  Створює головне меню для управління потягами, де можна буде додати, переглянути, видалити потяги
    def manage_trains_menu(self):
        self.clear_window()
        self.train_menu = tk.Frame(self.root)
        self.train_menu.pack(pady=20)

        tk.Button(self.train_menu, text="Додати потяг", command=self.add_train, width=20).pack(pady=10)
        tk.Button(self.train_menu, text="Переглянути всі потяги", command=self.view_trains, width=20).pack(pady=10)
        tk.Button(self.train_menu, text="Назад", command=self.back_callback, width=20).pack(pady=10)

    #  Створює вікно для додавання нового потягу з полями для введеня даних
    def add_train(self):
        self.clear_window()
        self.add_train_menu = tk.Frame(self.root)
        self.add_train_menu.pack(pady=20)

        tk.Label(self.add_train_menu, text="Пункт відправки:").pack()
        self.origin_entry = tk.Entry(self.add_train_menu)
        self.origin_entry.pack()

        tk.Label(self.add_train_menu, text="Пункт призначення:").pack()
        self.destination_entry = tk.Entry(self.add_train_menu)
        self.destination_entry.pack()

        tk.Label(self.add_train_menu, text="Назва:").pack()
        self.name_entry = tk.Entry(self.add_train_menu)
        self.name_entry.pack()

        tk.Label(self.add_train_menu, text="Дата:").pack()
        self.date_entry = tk.Entry(self.add_train_menu)
        self.date_entry.pack()

        tk.Button(self.add_train_menu, text="Додати потяг", command=self.save_train, width=20).pack(pady=10)
        tk.Button(self.add_train_menu, text="Назад", command=self.manage_trains_menu, width=20).pack(pady=10)

    #  Зберігає потяг у базі даних після заповнення відповідних полів
    def save_train(self):
        origin = self.origin_entry.get()
        destination = self.destination_entry.get()
        name = self.name_entry.get()
        date = self.date_entry.get()

        if origin and destination and name and date:
            execute_query('INSERT INTO Train (origin, destination, name, date) VALUES (?, ?, ?, ?)',
                          (origin, destination, name, date))
            messagebox.showinfo("Успіх!", "Потяг успішно додано!")
            self.origin_entry.delete(0, tk.END)
            self.destination_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Помилка", "Не всі поля заповнені!")

    #  Відображає усі потяги з додатковою інформацією про вагони та бронювання
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
                available_seats = int(wagon[2]) - len(booked_seats)
                booked_percentage = (len(booked_seats) / int(wagon[2])) * 100 if int(wagon[2]) > 0 else 0
                wagon_info.append(
                    f"Вагон {wagon[1]}(заброньовані номери): {', '.join(map(str, booked_seats)) if booked_seats else 'Немає заброньованих'}. "
                    f"Вільних місць: {available_seats}, Заброньовано: {booked_percentage:.2f}%")

            train_info_frame = tk.Frame(self.view_trains_menu)
            train_info_frame.pack(pady=5)

            train_info = f"ID Потягу: {train[0]}, Назва: {train[3]}, Звідки: {train[1]}, Куди: {train[2]}," \
                         f" Дата: {train[4]}\n{', '.join(wagon_info)}"
            tk.Label(train_info_frame, text=train_info, wraplength=1000, justify="left").pack(side="left")

            tk.Button(train_info_frame, text="Видалити потяг", command=lambda t_id=train[0]: self.delete_train(t_id), width=20).pack(pady=5)

        tk.Button(self.view_trains_menu, text="Назад", command=self.manage_trains_menu, width=20).pack(pady=10)

    #  Видаляє потяг та пов'язані з ним вагони але за умови що в ньому немає бронювань
    def delete_train(self, train_id):
        bookings_count = fetch_query('SELECT COUNT(*) FROM Booking WHERE train_id = ?', (train_id,))[0][0]

        if bookings_count > 0:
            messagebox.showerror("Помилка!", "Неможливо видалити потяг з наявними бронюваннями!")
        else:
            execute_query('DELETE FROM Wagon WHERE train_id = ?', (train_id,))
            execute_query('DELETE FROM Train WHERE id = ?', (train_id,))
            messagebox.showinfo("Успіх", "Потяг успішно видалено!")
            self.view_trains()

