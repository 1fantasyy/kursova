import tkinter as tk
from tkinter import messagebox
from database import fetch_query, execute_query

# Клас для управління бронюваннями у програмі "Залізнична каса"
class ManageBookings:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.create_widgets()
        self.manage_bookings_menu()

    #  Створює необхідні віджети (кнопки і фрейми) на головному вікні
    def create_widgets(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.font = ("Times New Roman", 16, "bold")

    #  Очищує вміст (content_frame) від всіх дочірніх віджетів.
    def clear_window(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    #  Відображає головне меню з кнопками управління бронюваннями
    def manage_bookings_menu(self):
        self.clear_window()

        self.add_button("Додати бронювання", self.add_booking)
        self.add_button("Переглянути бронювання", self.view_bookings)
        self.add_button("Відмінити бронювання", self.cancel_booking)
        self.add_button("Змінити бронювання", self.modify_booking)
        self.add_button("Переглянути всі потяги", self.view_trains)
        self.add_button("Назад", self.back_callback)

    #  Додає кнопку з заданим текстом і командою обробки подій.
    def add_button(self, text, command):
        button = tk.Button(self.button_frame, text=text, command=command, width=20, bg="#A1F7E3", bd=1, font=self.font)
        button.pack(side=tk.LEFT, padx=5, pady=5)

    #  Відображає інформацію про всі потяги з відповідними вагонами та бронюваннями.
    def view_trains(self):
        self.clear_window()
        trains = fetch_query('SELECT * FROM Train')

        for train in trains:
            wagons = fetch_query('SELECT id, number FROM Wagon WHERE train_id = ?', (train[0],))
            wagon_info = []
            for wagon in wagons:
                bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
                booked_seats = [booking[0] for booking in bookings]
                wagon_info.append(
                    f"Вагон {wagon[1]}: {', '.join(map(str, booked_seats)) if booked_seats else 'Всі місця вільні'}")

            train_info = f"ID потягу: {train[0]}, Назва: {train[3]}, Звідки: {train[1]}, Куди: {train[2]}, Дата: {train[4]}, Вагони: {', '.join(wagon_info)}"
            tk.Label(self.content_frame, text=train_info, font=self.font).pack(pady=5)

    #  Відображає форму для додавання нового бронювання.
    def add_booking(self):
        self.clear_window()

        tk.Label(self.content_frame, text="Оберіть потяг:", font=self.font).pack()
        self.train_var = tk.StringVar(self.content_frame)
        trains = fetch_query('SELECT id, name FROM Train')
        self.train_var.set("Оберіть потяг")
        train_options = [f"{train[0]} - {train[1]}" for train in trains]
        self.train_menu = tk.OptionMenu(self.content_frame, self.train_var, *train_options)
        self.train_menu.config(font=self.font)
        self.train_menu.pack()

        tk.Label(self.content_frame, text="Оберіть вагон:", font=self.font).pack()
        self.wagon_var = tk.StringVar(self.content_frame)
        self.wagon_menu = tk.OptionMenu(self.content_frame, self.wagon_var, "")
        self.wagon_menu.config(font=self.font)
        self.wagon_menu.pack()

        self.train_var.trace('w', self.update_wagon_menu)

        tk.Label(self.content_frame, text="Оберіть місце:", font=self.font).pack()
        self.seat_number_entry = tk.Entry(self.content_frame, font=self.font)
        self.seat_number_entry.pack()

        tk.Button(self.content_frame, text="Додати бронювання", command=self.save_booking, width=20, bg="#A1F7E3", bd=1, font=self.font).pack(pady=10)

    #  Оновлює випадаюче меню вагонів залежно від вибраного потягу.
    def update_wagon_menu(self, *args):
        train_id = self.train_var.get().split(" - ")[0]
        wagons = fetch_query('SELECT id, number, seats FROM Wagon WHERE train_id = ?', (train_id,))
        self.wagon_var.set("")
        menu = self.wagon_menu["menu"]
        menu.delete(0, "end")
        for wagon in wagons:
            bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
            booked_seats = [booking[0] for booking in bookings]
            menu.add_command(label=f"{wagon[0]} - {wagon[1]} (Заброньовані місця: {', '.join(map(str, booked_seats))})",
                             command=lambda value=f"{wagon[0]} - {wagon[1]} ({wagon[2]})": self.wagon_var.set(value))

    #  Зберігає нове бронювання в базі даних.
    def save_booking(self):
        train_id = self.train_var.get().split(" - ")[0]
        wagon_id, wagon_number, seats = self.wagon_var.get().split(" - ")[0], self.wagon_var.get().split(" - ")[1], int(self.wagon_var.get().split("(")[1].split(")")[0])
        seat_number = self.seat_number_entry.get()

    #  Перевірка заповненості полів
        if not train_id or not wagon_id or not seat_number:
            messagebox.showerror("Помилка", "Всі поля повинні бути заповнені!")
            return

    #  Перевірка що місце додатнє число та належить межам кількості місьц у вагоні
        if not seat_number.isdigit() or int(seat_number) <= 0 or int(seat_number) > seats:
            messagebox.showerror("Помилка", "Номер місця повинен бути додатнім та в межах кількості місць!")
            return

    #  Перевірка чи є місце вже заброньованим
        existing_bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon_id,))
        if int(seat_number) in [booking[0] for booking in existing_bookings]:
            messagebox.showerror("Помилка", "Це місце вже заброньовано або ви обираєте те саме місце!")
            return

    #  Бронювання місця
        execute_query('INSERT INTO Booking (train_id, wagon_id, seat_number) VALUES (?, ?, ?)',
                      (train_id, wagon_id, seat_number))
        messagebox.showinfo("Успіх", "Місце успішно заброньовано!")
        self.seat_number_entry.delete(0, tk.END)

    #  Відображає список всіх бронювань у системі.
    def view_bookings(self):
        self.clear_window()
        bookings = fetch_query('''SELECT b.id, b.train_id, b.wagon_id, b.seat_number, t.date 
                                  FROM Booking b 
                                  JOIN Train t ON b.train_id = t.id''')

        for booking in bookings:
            booking_info = f"ID Бронювання: {booking[0]}, ID Потягу: {booking[1]}, ID Вагону: {booking[2]}, Номер Місця: {booking[3]}, Дата: {booking[4]}"
            tk.Label(self.content_frame, text=booking_info, font=self.font).pack(pady=5)

    #  Відображає форму для відміни існуючого бронювання.
    def cancel_booking(self):
        self.clear_window()

        tk.Label(self.content_frame, text="Введіть ID бронюваня щоб відмінити:", font=self.font).pack()
        self.booking_id_entry = tk.Entry(self.content_frame, font=self.font)
        self.booking_id_entry.pack()

        tk.Button(self.content_frame, text="Відмінити бронювання", command=self.delete_booking, width=20, bg="#A1F7E3", bd=1, font=self.font).pack(pady=10)

    #  Видаляє обране бронювання з бази даних.
    def delete_booking(self):
        booking_id = self.booking_id_entry.get()

    #  Перевірка коректності ID броні
        if not booking_id:
            messagebox.showerror("Помилка", "Введіть коректне ID.")
            return

    #  Перевірка чи є в списку таке ID
        existing_booking = fetch_query('SELECT * FROM Booking WHERE id = ?', (booking_id,))
        if not existing_booking:
            messagebox.showerror("Помилка", "Такого ID не існує.")
            return

    #  Видалення бронювання
        execute_query('DELETE FROM Booking WHERE id = ?', (booking_id,))
        messagebox.showinfo("Успіх", "Бронювання успішно видалено!")
        self.booking_id_entry.delete(0, tk.END)

    #  Відображає форму для зміни існуючого бронювання
    def modify_booking(self):
        self.clear_window()

        tk.Label(self.content_frame, text="Введіть ID бронювання щоб змінити", font=self.font).pack()
        self.booking_id_entry = tk.Entry(self.content_frame, font=self.font)
        self.booking_id_entry.pack()

        tk.Label(self.content_frame, text="Новий Потяг:", font=self.font).pack()
        self.new_train_var = tk.StringVar(self.content_frame)
        trains = fetch_query('SELECT id, name FROM Train')
        self.new_train_var.set("Виберіть потяг")
        train_options = [f"{train[0]} - {train[1]}" for train in trains]
        self.new_train_menu = tk.OptionMenu(self.content_frame, self.new_train_var, *train_options)
        self.new_train_menu.config(font=self.font)
        self.new_train_menu.pack()

        tk.Label(self.content_frame, text="Новий вагон:", font=self.font).pack()
        self.new_wagon_var = tk.StringVar(self.content_frame)
        self.new_wagon_menu = tk.OptionMenu(self.content_frame, self.new_wagon_var, "")
        self.new_wagon_menu.config(font=self.font)
        self.new_wagon_menu.pack()

        self.new_train_var.trace('w', self.update_new_wagon_menu)

        tk.Label(self.content_frame, text="Нове місце:", font=self.font).pack()
        self.new_seat_number_entry = tk.Entry(self.content_frame, font=self.font)
        self.new_seat_number_entry.pack()

        tk.Button(self.content_frame, text="Змінити бронювання", command=self.update_booking, width=20, bg="#A1F7E3", bd=1, font=self.font).pack(pady=10)

    #  Оновлює випадаюче меню вагонів для зміни бронювання залежно від нового потягу.
    def update_new_wagon_menu(self, *args):
        train_id = self.new_train_var.get().split(" - ")[0]
        wagons = fetch_query('SELECT id, number, seats FROM Wagon WHERE train_id = ?', (train_id,))
        self.new_wagon_var.set("")
        menu = self.new_wagon_menu["menu"]
        menu.delete(0, "end")
        for wagon in wagons:
            bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (wagon[0],))
            booked_seats = [booking[0] for booking in bookings]
            menu.add_command(label=f"{wagon[0]} - {wagon[1]} (Заброньовані місця: {', '.join(map(str, booked_seats))})",
                             command=lambda value=f"{wagon[0]} - {wagon[1]} ({wagon[2]})": self.new_wagon_var.set(value))

    #  Змінює обране бронювання з новими даними в базі даних
    def update_booking(self):
        booking_id = self.booking_id_entry.get()
        new_train_id = self.new_train_var.get().split(" - ")[0]
        new_wagon_id, new_wagon_number, seats = self.new_wagon_var.get().split(" - ")[0], self.new_wagon_var.get().split(" - ")[1], int(self.new_wagon_var.get().split("(")[1].split(")")[0])
        new_seat_number = self.new_seat_number_entry.get()

    #  Поле айді пусте
        if not booking_id:
            messagebox.showerror("Похибка", "Введіть ID бронювання.")
            return

    #  Перевірка чи ID існує
        existing_booking = fetch_query('SELECT * FROM Booking WHERE id = ?', (booking_id,))
        if not existing_booking:
            messagebox.showerror("Похибка", "Такого ID не існує.")
            return

    #  Перевірка заповненості всіх полів
        if not new_train_id or not new_wagon_id or not new_seat_number:
            messagebox.showerror("Похибка", "Заповніть всі поля!")
            return

    #  Місце у вагоні повинно бути додатнім та в межах кількості місць вагону
        if not new_seat_number.isdigit() or int(new_seat_number) <= 0 or int(new_seat_number) > seats:
            messagebox.showerror("Похибка", "Місце вагону повинно бути додатнім там в межах кількості місць!")
            return

    #  Перевірка вільності місця
        existing_bookings = fetch_query('SELECT seat_number FROM Booking WHERE wagon_id = ?', (new_wagon_id,))
        if int(new_seat_number) in [booking[0] for booking in existing_bookings]:
            messagebox.showerror("Похибка", "Це місце вже зайняте!")
            return

    #  Зміна бронювання
        execute_query('UPDATE Booking SET train_id = ?, wagon_id = ?, seat_number = ? WHERE id = ?',
                      (new_train_id, new_wagon_id, new_seat_number, booking_id))
        messagebox.showinfo("Успіх", "Бронювання змінено!")
        self.booking_id_entry.delete(0, tk.END)
        self.new_seat_number_entry.delete(0, tk.END)








