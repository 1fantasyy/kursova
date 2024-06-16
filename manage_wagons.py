import tkinter as tk
from tkinter import messagebox
from database import execute_query, fetch_query

# Клас для управління вагонами у програмі "Залізнична каса"
class ManageWagons:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        # Створення основного фрейму
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для кнопок функціоналу
        self.menu_frame = tk.Frame(self.main_frame)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Контейнер для центрування кнопок
        self.button_container = tk.Frame(self.menu_frame)
        self.button_container.pack(anchor="center")

        # Кнопки з оновленими параметрами
        tk.Button(self.button_container, text="Додати вагон", command=self.show_add_wagon_form, font=("Times New Roman", 14, "bold"),
                  width=30, bg="#A1F7E3").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.button_container, text="Переглянути всі вагони", command=self.show_wagons, font=("Times New Roman", 14, "bold"),
                  width=30, bg="#A1F7E3").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.button_container, text="Назад", command=self.back_callback, font=("Times New Roman", 14, "bold"),
                  width=30, bg="#A1F7E3").pack(side=tk.LEFT, padx=10, pady=10)

        # Фрейм для контенту, який буде змінюватися
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    # Очищає фрейм контенту від дочірніх віджетів
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # Показує форму для додавання нового вагону
    def show_add_wagon_form(self):
        self.clear_content_frame()

        tk.Label(self.content_frame, text="Оберіть потяг:", font=("Times New Roman", 14, "bold")).pack()
        self.train_var = tk.StringVar(self.content_frame)
        trains = fetch_query('SELECT id, name FROM Train')
        self.train_var.set("Оберіть потяг")
        train_options = [f"{train[0]} - {train[1]}" for train in trains]
        self.train_menu = tk.OptionMenu(self.content_frame, self.train_var, *train_options)
        self.train_menu.pack()

        tk.Label(self.content_frame, text="Задайте номер вагону:", font=("Times New Roman", 14, "bold")).pack()
        self.wagon_number_entry = tk.Entry(self.content_frame, font=("Times New Roman", 14))
        self.wagon_number_entry.pack()

        tk.Label(self.content_frame, text="Кількість місць у вагоні:", font=("Times New Roman", 14, "bold")).pack()
        self.seats_entry = tk.Entry(self.content_frame, font=("Times New Roman", 14))
        self.seats_entry.pack()

        tk.Button(self.content_frame, text="Додати вагон", command=self.save_wagon, font=("Times New Roman", 14, "bold"),
                  width=30, bg="#A1F7E3").pack(pady=10)

    # Зберігає вагон у базі даних після заповнення відповідних полів
    def save_wagon(self):
        train_id = self.train_var.get().split(" - ")[0]
        number = self.wagon_number_entry.get()
        seats = self.seats_entry.get()

    #  Перевірка заповненості полів
        if not train_id or not number or not seats:
            messagebox.showerror("Помилка", "Не всі поля заповнені!")
            return
    #  Перевірка що число введене як номер вагону не є від'ємним
        if not number.isdigit() or int(number) <= 0:
            messagebox.showerror("Помилка", "Номер вагону має бути додатним числом!")
            return
    #  Перевірка що кількість місць додатнє число
        if not seats.isdigit() or int(seats) <= 0:
            messagebox.showerror("Помилка", "Кількість місць має бути додатним числом!")
            return
    #  Перевірка чи є вже потяг з таким номером у потязі
        existing_wagons = fetch_query('SELECT number FROM Wagon WHERE train_id = ?', (train_id,))
        if any(int(wagon[0]) == int(number) for wagon in existing_wagons):
            messagebox.showerror("Помилка", "Вагон з таким номером вже існує у цьому потязі!")
            return
    #  Додавання вагону
        execute_query('INSERT INTO Wagon (train_id, number, seats) VALUES (?, ?, ?)', (train_id, int(number), int(seats)))
        messagebox.showinfo("Успіх", "Вагон успішно додано!")
        self.wagon_number_entry.delete(0, tk.END)
        self.seats_entry.delete(0, tk.END)

    # Показує список всіх вагонів з обмеженою інформацією
    def show_wagons(self):
        self.clear_content_frame()

        wagons = fetch_query('SELECT * FROM Wagon')

        for wagon in wagons:
            wagon_info_frame = tk.Frame(self.content_frame)
            wagon_info_frame.pack(pady=5, padx=10, fill=tk.X)

            train = fetch_query('SELECT * FROM Train WHERE id = ?', (wagon[1],))[0]
            train_info = f"Звідки: {train[1]}, Куди: {train[2]}, Назва: {train[3]}, Дата: {train[4]}"

            wagon_info = f"{train_info}, Номер вагону: {wagon[2]}, Кількість місць: {wagon[3]}"
            tk.Label(wagon_info_frame, text=wagon_info, wraplength=1000, justify="left", font=("Times New Roman", 16)).pack(side=tk.LEFT)

            tk.Button(wagon_info_frame, text="Детальніша інформація", command=lambda w_id=wagon[0]: self.show_wagon_details(w_id), font=("Times New Roman", 16, "bold"), width=20, bd="1", bg="#A1F7E3", activebackground="#C7F9EE").pack(side=tk.RIGHT, padx=5, pady=5)




    # Показує детальну інформацію про обраний вагон
    def show_wagon_details(self, wagon_id):
        self.clear_content_frame()

        wagon = fetch_query('SELECT * FROM Wagon WHERE id = ?', (wagon_id,))[0]
        train = fetch_query('SELECT * FROM Train WHERE id = ?', (wagon[1],))[0]
        bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon_id,))
        booked_seats = [booking[0] for booking in bookings]
        available_seats = int(wagon[3]) - len(booked_seats)

        train_info = f"Пункт відправки: {train[1]}, Пункт призначення: {train[2]}, Назва: {train[3]}, Дата: {train[4]}"
        wagon_info = f"{train_info}, Номер вагону: {wagon[2]}, Кількість місць: {wagon[3]}, " \
                     f"Зайняті місця: {', '.join(map(str, booked_seats)) if booked_seats else 'Відсутні'}, " \
                     f"Вільних місць: {available_seats}"

        wagon_info_frame = tk.Frame(self.content_frame)
        wagon_info_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(wagon_info_frame, text=wagon_info, wraplength=1000, justify="left", font=("Times New Roman", 14)).pack(
            side=tk.LEFT)

        seat_frame = tk.Frame(self.content_frame)
        seat_frame.pack(pady=10)

        # Графічний вивід місць, обмеження на рядок в 15 місць
        row_length = 15
        for i, seat_num in enumerate(range(1, int(wagon[3]) + 1)):
            seat_color = "red" if seat_num in booked_seats else "green"
            seat_label = tk.Label(seat_frame, text=str(seat_num), bg=seat_color, width=4, height=2, relief=tk.RAISED,
                                  font=("Times New Roman", 10, "bold"))
            seat_label.grid(row=i // row_length, column=i % row_length, padx=5, pady=5)

        if not booked_seats:
            tk.Button(self.content_frame, text="Видалити вагон", command=lambda w_id=wagon_id: self.delete_wagon(w_id),
                      font=("Times New Roman", 14, "bold"), width=30, bd="1", bg="#A1F7E3",
                      activebackground="#C7F9EE").pack(pady=10)

        tk.Button(self.content_frame, text="Назад до вагонів", command=self.show_wagons,
                  font=("Times New Roman", 14, "bold"), width=30, bd="1", bg="#A1F7E3",
                  activebackground="#C7F9EE").pack(pady=10)

        # Видаляє вагон з бази даних

    def delete_wagon(self, wagon_id):
        bookings_count = fetch_query('SELECT COUNT(*) FROM Booking WHERE wagon_id = ?', (wagon_id,))[0][0]

        if bookings_count > 0:
            messagebox.showerror("Помилка!", "Неможливо видалити вагон з наявними бронюваннями!")
        else:
            execute_query('DELETE FROM Wagon WHERE id = ?', (wagon_id,))
            messagebox.showinfo("Успіх", "Вагон успішно видалено!")
            self.show_wagons()










