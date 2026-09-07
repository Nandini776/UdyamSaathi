import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DB_NAME = "rural_store.db"

def seed_1076_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Ensure Schema Exists
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

    # 2. Force Insert/Update Demo User
    demo_shop_id = "SHOP-9001"
    cursor.execute('''
        INSERT OR REPLACE INTO users (shop_id, owner_name, shop_name, password)
        VALUES (?, ?, ?, ?)
    ''', (demo_shop_id, "Ramesh Kumar", "Ramesh Kirana Store", "password123"))

    # 3. Clear old transactions for SHOP-9001
    cursor.execute("DELETE FROM transactions WHERE shop_id = ?", (demo_shop_id,))

    # 4. Generate 1,076 Realistic Transactions
    np.random.seed(42)
    TOTAL_ROWS = 1076
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    random_dates = [
        start_date + timedelta(seconds=int(np.random.randint(0, int((end_date - start_date).total_seconds()))))
        for _ in range(TOTAL_ROWS)
    ]
    random_dates.sort()
    formatted_dates = [d.strftime('%Y-%m-%d') for d in random_dates]

    items = ["Chawal(Rice)", "Aata(Wheat Flour)", "Daal(Lentils)", "Cooking Oil(Tel)", "Tea & Biscuits", "Sugar"]
    types = np.random.choice(["Income", "Expense"], size=TOTAL_ROWS, p=[0.75, 0.25])
    
    transactions = []
    for i in range(TOTAL_ROWS):
        item = np.random.choice(items)
        tx_type = types[i]
        
        if tx_type == "Income":
            amount = round(float(np.random.uniform(100.0, 950.0)), 2)
        else:
            amount = round(float(np.random.uniform(200.0, 1500.0)), 2)
            
        transactions.append((demo_shop_id, formatted_dates[i], tx_type, item, amount))

    # 5. Insert rows tagged specifically with SHOP-9001
    cursor.executemany(
        "INSERT INTO transactions (shop_id, date, type, item, amount) VALUES (?, ?, ?, ?, ?)",
        transactions
    )

    conn.commit()
    conn.close()

    print(f"✅ Success! 1076 transactions seeded for {demo_shop_id}. User credentials activated!")

if __name__ == "__main__":
    seed_1076_data()