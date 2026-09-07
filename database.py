import sqlite3
import hashlib
import pandas as pd
import os

DB_NAME = "rural_store.db"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            shop_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            shop_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (shop_id) REFERENCES users (shop_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_credit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            due_amount REAL NOT NULL,
            due_date TEXT NOT NULL,
            FOREIGN KEY (shop_id) REFERENCES users (shop_id)
        )
    ''')
    conn.commit()

    # Check if database is empty; if so, trigger auto-seeding
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        try:
            from generate_data import seed_complete_enterprise_data
            seed_complete_enterprise_data()
        except ImportError:
            pass

def register_user(owner_name, shop_name, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    import random
    allotted_shop_id = f"SHOP-{random.randint(1000, 9999)}"
    
    try:
        cursor.execute(
            "INSERT INTO users (shop_id, owner_name, shop_name, password) VALUES (?, ?, ?, ?)",
            (allotted_shop_id, owner_name, shop_name, hash_password(password))
        )
        conn.commit()
        return True, allotted_shop_id
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def authenticate_user(shop_id, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT owner_name, shop_name FROM users WHERE shop_id = ? AND password = ?", (shop_id, hashed))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True, {"owner_name": user[0], "shop_name": user[1]}
    return False, None

def fetch_shop_transactions(shop_id):
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT date, type, item, amount FROM transactions WHERE shop_id = ? ORDER BY date ASC"
    df = pd.read_sql_query(query, conn, params=(shop_id,))
    conn.close()
    return df

def insert_shop_transaction(shop_id, date, tx_type, item, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (shop_id, date, type, item, amount) VALUES (?, ?, ?, ?, ?)",
        (shop_id, date, tx_type, item, amount)
    )
    conn.commit()
    conn.close()

def add_credit_entry(shop_id, customer_name, phone, amount, due_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO customer_credit (shop_id, customer_name, phone, due_amount, due_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (shop_id, customer_name, phone, amount, due_date))
    conn.commit()
    conn.close()

def fetch_credit_entries(shop_id):
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT id, customer_name, phone, due_amount, due_date FROM customer_credit WHERE shop_id = ?"
    df = pd.read_sql_query(query, conn, params=(shop_id,))
    conn.close()
    return df

init_db()