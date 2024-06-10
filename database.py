import sqlite3

def connect_db():
    return sqlite3.connect("train_booking.db")

def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def create_tables():
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

# Виклик функції для створення таблиць
create_tables()



