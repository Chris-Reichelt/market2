import sqlite3
from utils import hash_password  # Import from utils.py

def get_connection():
    conn = sqlite3.connect('market.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        user_type TEXT NOT NULL
    )
    ''')

    # Create companies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        shares INTEGER,
        market_price REAL,
        buy_price REAL
    );
    ''')

    # Create bids table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bids (
        bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        company_id INTEGER,
        num_shares INTEGER,
        bid_price REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES users(username),
        FOREIGN KEY(company_id) REFERENCES companies(company_id)
    );
    ''')

    # Insert default admin user if not exists
    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password, email, user_type) VALUES (?, ?, ?, ?)
    ''', ('admin', hash_password('admin123'), 'reicheltcm@gmail.com', 'Admin'))

    # Insert default user if not exists
    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password, email, user_type) VALUES (?, ?, ?, ?)
    ''', ('user', hash_password('user123'),'reicheltcm@gmail.com' 'User'))

    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, password, user_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                   (username, password, user_type))
    conn.commit()
    conn.close()

def add_company(name, shares, market_price, buy_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (name, shares, market_price, buy_price) VALUES (?, ?, ?, ?)",
                   (name, shares, market_price, buy_price))
    conn.commit()
    conn.close()

def get_companies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    conn.close()
    return companies

def place_bid(username, company_id, num_shares, bid_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bids (username, company_id, num_shares, bid_price) VALUES (?, ?, ?, ?)",
                   (username, company_id, num_shares, bid_price))
    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_bid(username, company_name, bid_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bids (username, company_name, bid_amount)
        VALUES (?, ?, ?)
    ''', (username, company_name, bid_amount))
    conn.commit()
    conn.close()

def get_company_list():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM companies")
    companies = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return companies
