import sqlite3
from datetime import datetime
import os

def get_connection(db_path="data/app_data.db"):
    # 确保数据目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # 用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            email TEXT UNIQUE,
            name TEXT
        )
    ''')
    
    # 投资场景表
    c.execute('''
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data JSON,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 房产信息表
    c.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_id INTEGER,
            property_type TEXT,
            purchase_price REAL,
            down_payment REAL,
            mortgage_rate REAL,
            mortgage_term INTEGER,
            rental_income REAL,
            expected_appreciation REAL,
            vacancy_rate REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
        )
    ''')
    
    # 支出表
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            description TEXT,
            expense_type TEXT,
            amount REAL,
            date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(id)
        )
    ''')
    
    # 收入表
    c.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            description TEXT,
            income_type TEXT,
            amount REAL,
            date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(id)
        )
    ''')
    
    # 贷款信息表
    c.execute('''
        CREATE TABLE IF NOT EXISTS mortgages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            loan_amount REAL,
            interest_rate REAL,
            term_years INTEGER,
            start_date TEXT,
            end_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(id)
        )
    ''')
    
    # 再融资记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS refinances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            original_mortgage_id INTEGER,
            new_loan_amount REAL,
            new_interest_rate REAL,
            new_term_years INTEGER,
            refinance_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties(id),
            FOREIGN KEY (original_mortgage_id) REFERENCES mortgages(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# 用户相关函数
def create_user(email, name):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (email, name) VALUES (?, ?)', (email, name))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

# 场景相关函数
def create_scenario(user_id, name, data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO scenarios (user_id, name, data) VALUES (?, ?, ?)',
              (user_id, name, data))
    scenario_id = c.lastrowid
    conn.commit()
    conn.close()
    return scenario_id

# 房产相关函数
def create_property(scenario_id, property_data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO properties (
            scenario_id, property_type, purchase_price, down_payment,
            mortgage_rate, mortgage_term, rental_income,
            expected_appreciation, vacancy_rate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        scenario_id,
        property_data['property_type'],
        property_data['purchase_price'],
        property_data['down_payment'],
        property_data['mortgage_rate'],
        property_data['mortgage_term'],
        property_data['rental_income'],
        property_data['expected_appreciation'],
        property_data['vacancy_rate']
    ))
    property_id = c.lastrowid
    conn.commit()
    conn.close()
    return property_id

# 支出相关函数
def create_expense(property_id, type, amount, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (property_id, expense_type, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (property_id, type, amount, date))
    expense_id = c.lastrowid
    conn.commit()
    conn.close()
    return expense_id

# 收入相关函数
def create_income(property_id, type, amount, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO incomes (property_id, income_type, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (property_id, type, amount, date))
    income_id = c.lastrowid
    conn.commit()
    conn.close()
    return income_id

# 贷款相关函数
def create_mortgage(property_id, loan_amount, interest_rate, term, start_date, end_date):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO mortgages (
            property_id, loan_amount, interest_rate,
            term_years, start_date, end_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        property_id,
        loan_amount,
        interest_rate,
        term,
        start_date,
        end_date
    ))
    mortgage_id = c.lastrowid
    conn.commit()
    conn.close()
    return mortgage_id

# 再融资相关函数
def create_refinance(property_id, original_mortgage_id, refinance_data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO refinances (
            property_id, original_mortgage_id, new_loan_amount,
            new_interest_rate, new_term_years, refinance_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        property_id,
        original_mortgage_id,
        refinance_data['new_loan_amount'],
        refinance_data['new_interest_rate'],
        refinance_data['new_term_years'],
        refinance_data['refinance_date']
    ))
    refinance_id = c.lastrowid
    conn.commit()
    conn.close()
    return refinance_id

# 查询函数
def get_property_expenses(property_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM expenses WHERE property_id=?', (property_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_property_incomes(property_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM incomes WHERE property_id=?', (property_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_property_mortgages(property_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM mortgages WHERE property_id=?', (property_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_scenario_properties(scenario_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM properties WHERE scenario_id=?', (scenario_id,))
    rows = c.fetchall()
    conn.close()
    return rows 