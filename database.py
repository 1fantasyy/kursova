import sqlite3

def connect_db():
    """
    Підключення до бази даних SQLite з файлом "train_booking.db".

    Повертає:
    --------
    conn : sqlite3.Connection
        Об'єкт підключення до бази даних.

    Виключення:
    ----------
    Виняток `sqlite3.Error` може виникати при невдалому з'єднанні з базою даних.
    """
    return sqlite3.connect("train_booking.db")

def execute_query(query, params=()):
    """
    Виконання SQL-запиту на базі даних.

    Параметри:
    ----------
    query : str
        SQL-запит для виконання.
    params : tuple, optional
        Параметри для передачі у запит (за замовчуванням пустий кортеж).


    Виключення:
    ----------
    Виняток `sqlite3.Error` може виникати при невдалому виконанні запиту.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    """
    Виконання SQL-запиту на базі даних та отримання результатів.

    Параметри:
    ----------
    query : str
        SQL-запит для виконання.
    params : tuple, optional
        Параметри для передачі у запит (за замовчуванням пустий кортеж).

    Повертає:
    --------
    results : list
        Список кортежів з результатами запиту.

    Виключення:
    ----------
    Виняток `sqlite3.Error` може виникати при невдалому виконанні запиту.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def create_tables():
    """
    Створення таблиць у базі даних, якщо вони ще не існують.

    Параметри:
    ----------
    Немає параметрів.

    Повертає:
    --------
    Немає повернення значення.

    Виключення:
    ----------
    Виняток `sqlite3.Error` може виникати при невдалому виконанні запитів на створення таблиць.
    """
    execute_query('''
    CREATE TABLE IF NOT EXISTS Train (
        id INTEGER PRIMARY KEY,
        origin TEXT,
        destination TEXT,
        name TEXT,
        date TEXT
    )
    ''')

    execute_query('''
    CREATE TABLE IF NOT EXISTS Wagon (
        id INTEGER PRIMARY KEY,
        train_id INTEGER,
        number TEXT,
        seats INTEGER,
        FOREIGN KEY(train_id) REFERENCES Train(id)
    )
    ''')

    execute_query('''
    CREATE TABLE IF NOT EXISTS Booking (
        id INTEGER PRIMARY KEY,
        train_id INTEGER,
        wagon_id INTEGER,
        seat_number INTEGER,
        date TEXT,
        FOREIGN KEY(train_id) REFERENCES Train(id),
        FOREIGN KEY(wagon_id) REFERENCES Wagon(id)
    )
    ''')

# Виклик функції для створення таблиць при запуску скрипту
create_tables()







