import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DB_NAME = "rural_store.db"

def generate_1076_dataset():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Database Schema Setup
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

    # 2. Add Demo User (SHOP-9001)
    demo_shop_id = "SHOP-9001"
    cursor.execute("SELECT shop_id FROM users WHERE shop_id = ?", (demo_shop_id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (shop_id, owner_name, shop_name, password) VALUES (?, ?, ?, ?)",
            (demo_shop_id, "Ramesh Kumar", "Ramesh Kirana Store", "password123")
        )
    
    # Clear previous entries for clean seeding
    cursor.execute("DELETE FROM transactions WHERE shop_id = ?", (demo_shop_id,))

    # 3. Generate Exact 1,076 Transactions Data
    np.random.seed(42)
    TOTAL_ROWS = 1076
    
    # 90 Days date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    # Generate random timestamps spanning 90 days
    random_dates = [
        start_date + timedelta(seconds=int(np.random.randint(0, int((end_date - start_date).total_seconds()))))
        for _ in range(TOTAL_ROWS)
    ]
    random_dates.sort()
    formatted_dates = [d.strftime('%Y-%m-%d') for d in random_dates]

    # Inventory Categories & Amounts
    items = ["Chawal(Rice)", "Aata(Wheat Flour)", "Daal(Lentils)", "Cooking Oil(Tel)", "Tea & Biscuits", "Sugar"]
    
    # 75% Income (Sales), 25% Expense (Procurement)
    types = np.random.choice(["Income", "Expense"], size=TOTAL_ROWS, p=[0.75, 0.25])
    
    transactions = []
    for i in range(TOTAL_ROWS):
        item = np.random.choice(items)
        tx_type = types[i]
        
        # Realistic Kirana pricing distribution
        if tx_type == "Income":
            amount = round(float(np.random.uniform(50.0, 850.0)), 2)
        else:
            amount = round(float(np.random.uniform(300.0, 2500.0)), 2)
            
        transactions.append((demo_shop_id, formatted_dates[i], tx_type, item, amount))

    # 4. Insert 1,076 Rows into SQLite Database
    cursor.executemany(
        "INSERT INTO transactions (shop_id, date, type, item, amount) VALUES (?, ?, ?, ?, ?)",
        transactions
    )

    conn.commit()
    conn.close()

    print(f"✅ Success! Exactly {TOTAL_ROWS} transaction rows seeded for {demo_shop_id} into '{DB_NAME}'.")

if __name__ == "__main__":
    generate_1076_dataset()