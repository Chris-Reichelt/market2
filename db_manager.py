import sqlite3

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
        username TEXT PRIMARY KEY,
        password TEXT,
        user_type TEXT
    );
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
    INSERT OR IGNORE INTO users (username, password, user_type) VALUES (?, ?, ?)
    ''', ('admin', hash_password('admin123'), 'Admin'))

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
