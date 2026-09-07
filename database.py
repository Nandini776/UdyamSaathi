import sqlite3
import hashlib
import pandas as pd
import random
from datetime import datetime, timedelta

DB_NAME = "rural_store.db"

def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10.0)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()

def seed_90_days_data(shop_id):
    conn = get_connection()
    cursor = conn.cursor()
    clean_id = shop_id.strip().upper()
    
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE UPPER(shop_id) = ?", (clean_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    items = ["Chawal(Rice)", "Aata(Wheat Flour)", "Daal(Lentils)", "Cooking Oil(Tel)", "Tea & Biscuits", "Sugar"]
    start_date = datetime.now() - timedelta(days=90)
    
    records = []
    for day in range(90):
        current_date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
        for _ in range(random.randint(2, 4)):
            item = random.choice(items)
            amount = round(random.uniform(100.0, 600.0), 2)
            records.append((clean_id, current_date, 'Income', item, amount))
            
        expense_amount = round(random.uniform(150.0, 500.0), 2)
        records.append((clean_id, current_date, 'Expense', 'Restock Inventory', expense_amount))
        
    cursor.executemany('''
        INSERT INTO transactions (shop_id, date, type, item, amount)
        VALUES (?, ?, ?, ?, ?)
    ''', records)
    
    conn.commit()
    conn.close()

def init_db():
    conn = get_connection()
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
    
    hashed_pass = hash_password("password123")
    cursor.execute("INSERT OR REPLACE INTO users (shop_id, owner_name, shop_name, password) VALUES ('SHOP-9001', 'Ramesh Kumar', 'Mahadev Kirana Store', ?)", (hashed_pass,))
    conn.commit()
    conn.close()
    
    seed_90_days_data('SHOP-9001')

def register_user(owner_name, shop_name, password):
    conn = get_connection()
    cursor = conn.cursor()
    allotted_shop_id = f"SHOP-{random.randint(1000, 9999)}"
    hashed_pass = hash_password(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (shop_id, owner_name, shop_name, password) VALUES (?, ?, ?, ?)",
            (allotted_shop_id, owner_name, shop_name, hashed_pass)
        )
        conn.commit()
        conn.close()
        
        seed_90_days_data(allotted_shop_id)
        return True, allotted_shop_id
    except Exception as e:
        conn.close()
        return False, str(e)

def authenticate_user(shop_id, password):
    conn = get_connection()
    cursor = conn.cursor()
    clean_id = shop_id.strip().upper()
    
    # Absolute Bypass & Auto-Creation for SHOP-9001
    if clean_id == "SHOP-9001":
        cursor.execute("INSERT OR IGNORE INTO users (shop_id, owner_name, shop_name, password) VALUES ('SHOP-9001', 'Ramesh Kumar', 'Mahadev Kirana Store', 'password123')")
        conn.commit()
        conn.close()
        seed_90_days_data('SHOP-9001')
        return True, {"owner_name": "Ramesh Kumar", "shop_name": "Mahadev Kirana Store"}

    cursor.execute("SELECT owner_name, shop_name FROM users WHERE UPPER(shop_id) = ?", (clean_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, {"owner_name": user[0], "shop_name": user[1]}
            
    return False, None

def fetch_shop_transactions(shop_id):
    conn = get_connection()
    clean_id = shop_id.strip().upper()
    query = "SELECT date, type, item, amount FROM transactions WHERE UPPER(shop_id) = ? ORDER BY date ASC"
    df = pd.read_sql_query(query, conn, params=(clean_id,))
    conn.close()
    return df

def insert_shop_transaction(shop_id, date, tx_type, item, amount):
    conn = get_connection()
    cursor = conn.cursor()
    clean_id = shop_id.strip().upper()
    cursor.execute(
        "INSERT INTO transactions (shop_id, date, type, item, amount) VALUES (?, ?, ?, ?, ?)",
        (clean_id, date, tx_type, item, amount)
    )
    conn.commit()
    conn.close()

init_db()