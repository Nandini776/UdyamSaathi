import sqlite3
import random
import pandas as pd

DB_NAME = "rural_store.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            shop_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            shop_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Transactions Table with Foreign Key
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
    conn.commit()
    conn.close()

# Automatic Unique Shop ID Generator
def generate_unique_shop_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    while True:
        random_num = random.randint(1000, 9999)
        new_id = f"SHOP-{random_num}"
        cursor.execute("SELECT shop_id FROM users WHERE shop_id = ?", (new_id,))
        if not cursor.fetchone():
            conn.close()
            return new_id

def register_user(owner_name, shop_name, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    allotted_shop_id = generate_unique_shop_id()
    
    try:
        cursor.execute(
            "INSERT INTO users (shop_id, owner_name, shop_name, password) VALUES (?, ?, ?, ?)",
            (allotted_shop_id, owner_name, shop_name, password)
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
    cursor.execute("SELECT owner_name, shop_name FROM users WHERE shop_id = ? AND password = ?", (shop_id, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True, {"owner_name": user[0], "shop_name": user[1]}
    return False, None

def fetch_shop_transactions(shop_id):
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT date, type, item, amount FROM transactions WHERE shop_id = ?"
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

# Run database setup
init_db()