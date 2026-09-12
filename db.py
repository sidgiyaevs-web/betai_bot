import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "bot.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            stars INTEGER DEFAULT 1000,
            crystals INTEGER DEFAULT 0,
            total_opened INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            total_won INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            item_emoji TEXT,
            item_value INTEGER,
            item_rarity TEXT,
            case_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            case_id TEXT,
            item_name TEXT,
            item_emoji TEXT,
            item_value INTEGER,
            price INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_or_create_user(user_id, username="", first_name=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute(
            "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        conn.commit()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = c.fetchone()
    else:
        c.execute(
            "UPDATE users SET username = ?, first_name = ? WHERE user_id = ?",
            (username, first_name, user_id)
        )
        conn.commit()
    conn.close()
    return dict(row)

def get_user(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_balance(user_id, stars_delta=0, crystals_delta=0):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE users SET stars = stars + ?, crystals = crystals + ? WHERE user_id = ?",
        (stars_delta, crystals_delta, user_id)
    )
    conn.commit()
    conn.close()

def update_stats(user_id, opened=0, spent=0, won=0):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE users SET total_opened = total_opened + ?, total_spent = total_spent + ?, total_won = total_won + ? WHERE user_id = ?",
        (opened, spent, won, user_id)
    )
    conn.commit()
    conn.close()

def add_to_inventory(user_id, item_name, item_emoji, item_value, item_rarity, case_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO inventory (user_id, item_name, item_emoji, item_value, item_rarity, case_id) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, item_name, item_emoji, item_value, item_rarity, case_id)
    )
    conn.commit()
    conn.close()

def get_inventory(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def remove_from_inventory(item_id, user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id = ? AND user_id = ?", (item_id, user_id))
    conn.commit()
    conn.close()

def add_history(user_id, case_id, item_name, item_emoji, item_value, price):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (user_id, case_id, item_name, item_emoji, item_value, price) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, case_id, item_name, item_emoji, item_value, price)
    )
    conn.commit()
    conn.close()

def get_history(user_id, limit=50):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

init_db()
