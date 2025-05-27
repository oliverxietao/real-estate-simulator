import sqlite3

def get_connection(db_path="app_data.db"):
    return sqlite3.connect(db_path, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # 支出表
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            expense_type TEXT,
            amount REAL,
            date TEXT,
            property_id TEXT
        )
    ''')
    # 你可以按需添加更多表，如 scenario, assets 等
    conn.commit()
    conn.close()

def insert_expense(description, expense_type, amount, date, property_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (description, expense_type, amount, date, property_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (description, expense_type, amount, date, property_id))
    conn.commit()
    conn.close()

def get_expenses(property_id=None):
    conn = get_connection()
    c = conn.cursor()
    if property_id:
        c.execute('SELECT * FROM expenses WHERE property_id=?', (property_id,))
    else:
        c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    conn.close()
    return rows 