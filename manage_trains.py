import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import execute_query, fetch_query

# Клас для управління потягами у програмі "Залізнична каса"
class ManageTrains:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        # Створення основного фрейма
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для кнопок функціоналу
        self.menu_frame = tk.Frame(self.main_frame)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Контейнер для центрування кнопок
        self.button_container = tk.Frame(self.menu_frame)
        self.button_container.pack(anchor="center")

        button_font = ("Times New Roman", 16, "bold")

        tk.Button(self.button_container, text="Додати потяг", command=self.show_add_train_form, width=20, height=3,
                  font=button_font, bd="1", bg="#A1F7E3", activebackground="#C7F9EE").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_container, text="Переглянути всі потяги", command=self.show_trains, width=20, height=3,
                  font=button_font, bd="1", bg="#A1F7E3", activebackground="#C7F9EE").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_container, text="Назад", command=self.back_callback, width=20, height=3,
                  font=button_font, bd="1", bg="#A1F7E3", activebackground="#C7F9EE").pack(side=tk.LEFT, padx=5, pady=5)

        # Фрейм для контенту, який буде змінюватися
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    # Очищає фрейм контенту від дочірніх віджетів
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # Показує форму для додавання нового потягу
    def show_add_train_form(self):
        self.clear_content_frame()

        tk.Label(self.content_frame, text="Пункт відправки:", font=("Times New Roman", 14, "bold")).pack()
        self.origin_entry = tk.Entry(self.content_frame)
        self.origin_entry.pack()

        tk.Label(self.content_frame, text="Пункт призначення:", font=("Times New Roman", 14, "bold")).pack()
        self.destination_entry = tk.Entry(self.content_frame)
        self.destination_entry.pack()

        tk.Label(self.content_frame, text="Назва:", font=("Times New Roman", 14, "bold")).pack()
        self.name_entry = tk.Entry(self.content_frame)
        self.name_entry.pack()

        tk.Label(self.content_frame, text="Дата (день.місяць.рік):", font=("Times New Roman", 14, "bold")).pack()
        self.date_entry = DateEntry(self.content_frame, date_pattern='dd.mm.yyyy', font=("Times New Roman", 14, "bold"))
        self.date_entry.pack()

        tk.Button(self.content_frame, text="Додати потяг", command=self.save_train, width=20, height=3,
                  bd="1", bg="#A1F7E3", font=("Times New Roman", 16, "bold"), activebackground="#C7F9EE").pack(pady=10)

    # Зберігає потяг у базі даних після заповнення відповідних полів
    def save_train(self):
        origin = self.origin_entry.get()
        destination = self.destination_entry.get()
        name = self.name_entry.get()
        date = self.date_entry.get()

        if origin and destination and name and date:
            try:
                # Перевірка правильності формату дати
                date_obj = datetime.strptime(date, '%d.%m.%Y')
                # Перевірка, щоб дата не була з минулого
                if date_obj < datetime.now():
                    messagebox.showerror("Помилка", "Дата не може бути з минулого!")
                    return

                execute_query('INSERT INTO Train (origin, destination, name, date) VALUES (?, ?, ?, ?)',
                              (origin, destination, name, date))
                messagebox.showinfo("Успіх!", "Потяг успішно додано!")
                self.origin_entry.delete(0, tk.END)
                self.destination_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.date_entry.set_date(datetime.now())
            except ValueError:
                messagebox.showerror("Помилка", "Неправильний формат дати! Використовуйте формат день.місяць.рік")
        else:
            messagebox.showerror("Помилка", "Не всі поля заповнені!")

    # Показує список всіх потягів з обмеженою інформацією
    def show_trains(self):
        self.clear_content_frame()

        trains = fetch_query('SELECT * FROM Train')

        for train in trains:
            train_info_frame = tk.Frame(self.content_frame)
            train_info_frame.pack(pady=5, padx=10, fill=tk.X)

            train_info = f"Звідки: {train[1]}, Куди: {train[2]}, Назва: {train[3]}, Дата: {train[4]}"
            tk.Label(train_info_frame, text=train_info, wraplength=1000, font=("Times New Roman", 14, "bold"), justify="left").pack(side=tk.LEFT)

            tk.Button(train_info_frame, text="Переглянути детальніше", command=lambda t_id=train[0]: self.show_train_details(t_id), width=20,
                      bd="1", bg="#A1F7E3", font=("Times New Roman", 16, "bold"), activebackground="#C7F9EE").pack(side=tk.RIGHT, padx=5)



    # Показує детальну інформацію про обраний потяг
    def show_train_details(self, train_id):
        self.clear_content_frame()

        train = fetch_query('SELECT * FROM Train WHERE id = ?', (train_id,))[0]
        wagons = fetch_query('SELECT id, number, seats FROM Wagon WHERE train_id = ?', (train[0],))
        wagon_info = []
        for wagon in wagons:
            bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
            booked_seats = [booking[0] for booking in bookings]
            available_seats = int(wagon[2]) - len(booked_seats)
            booked_percentage = (len(booked_seats) / int(wagon[2])) * 100 if int(wagon[2]) > 0 else 0
            wagon_info.append(
                f"\nВагон {wagon[1]}(заброньовані номери): {', '.join(map(str, booked_seats)) if booked_seats else 'Немає заброньованих'}. "
                f"Вільних місць: {available_seats}, Заброньовано: {booked_percentage:.2f}%")

        train_info_frame = tk.Frame(self.content_frame)
        train_info_frame.pack(pady=5, padx=10, fill=tk.X)

        train_info = f"ID Потягу: {train[0]}, Назва: {train[3]}, Пункт відправки: {train[1]}, Пункт Призначення: {train[2]}, Дата: {train[4]}\n{', '.join(wagon_info)}"
        tk.Label(train_info_frame, text=train_info, wraplength=1000, justify="left", font=("Times New Roman", 14, "bold")).pack(side=tk.LEFT)

        tk.Button(train_info_frame, text="Видалити потяг", command=lambda t_id=train[0]: self.delete_train(t_id), width=20,
                  bd="1", bg="#A1F7E3", font=("Times New Roman", 16, "bold"), activebackground="#C7F9EE").pack(pady=5)

        tk.Button(self.content_frame, text="Повернутися назад до потягів", command=self.show_trains, width=30,
                  bd="1", bg="#A1F7E3", font=("Times New Roman", 16, "bold"), activebackground="#C7F9EE").pack(pady=10)

    # Видаляє потяг  з бази даних
    def delete_train(self, train_id):
        bookings_count = fetch_query('SELECT COUNT(*) FROM Booking WHERE train_id = ?', (train_id,))[0][0]

        if bookings_count > 0:
            messagebox.showerror("Помилка!", "Неможливо видалити потяг з наявними бронюваннями!")
        else:
            execute_query('DELETE FROM Wagon WHERE train_id = ?', (train_id,))
            execute_query('DELETE FROM Train WHERE id = ?', (train_id,))
            messagebox.showinfo("Успіх", "Потяг успішно видалено!")
            self.show_trains()







