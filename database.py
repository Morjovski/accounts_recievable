import sqlite3

def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def comm_close_db(conn):
    conn.commit()
    conn.close()

def create_db(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS sellers (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    user_id INTEGER NOT NULL UNIQUE,
    full_name TEXT NOT NULL
    );
                         
    CREATE TABLE IF NOT EXISTS ignore_buyers (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    buyer_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES sellers(id)
    );
                         
    CREATE TABLE IF NOT EXISTS ignore_comments (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    ignore_word TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES sellers(id)
    );
    """)

    comm_close_db(conn)

def add_user(conn, user_id, last_name, first_name):
    full_name = f"{last_name} {first_name}"

    cur = conn.cursor()

    cur.execute("INSERT INTO sellers (user_id, full_name) VALUES (?, ?)", (user_id, full_name))

    comm_close_db(conn)

def add_buyers(conn, buyer_names, user_id):
    cur = conn.cursor()

    for name in buyer_names:
        cur.execute("SELECT buyer_name, user_id FROM ignore_buyers WHERE user_id = ? AND buyer_name = ?", (user_id, name))
        exists_line = cur.fetchall()
        if not len(exists_line):
            cur.execute("INSERT INTO ignore_buyers (buyer_name, user_id) VALUES (?, ?)", (name, user_id))

    comm_close_db(conn)

def add_comments(conn, comment_words, user_id):
    cur = conn.cursor()

    for word in comment_words:
        cur.execute("SELECT ignore_word, user_id FROM ignore_comments WHERE user_id = ? AND ignore_word = ?", (user_id, word))
        exists_line = cur.fetchall()
        if not len(exists_line):
            cur.execute("INSERT INTO ignore_comments (ignore_word, user_id) VALUES (?, ?)", (word, user_id))

    comm_close_db(conn)

def delete_user(conn, user_id):
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM sellers WHERE user_id = ?", (user_id))
    exists_line = cur.fetchall()
    if len(exists_line):
        cur.execute("DELETE FROM sellers WHERE user_id = ?", (user_id,))

def delete_buyer(conn, buyers, user_id):
    cur = conn.cursor()

    for buyer in buyers:
        cur.execute("SELECT buyer_name, user_id FROM ignore_buyers WHERE buyer_name = ? AND user_id = ?", (buyer, user_id))
        exists_line = cur.fetchall()
        if len(exists_line):
            cur.execute("DELETE FROM ignore_buyers WHERE buyer_name = ? AND user_id = ?", (buyer, user_id))

def delete_comment(conn, comments, user_id):
    cur = conn.cursor()

    for comment in comments():
        cur.execute("SELECT ignore_word, user_id FROM ignore_comments WHERE ignore_word = ? AND user_id = ?", (comment, user_id))
        exists_line = cur.fetchall()
        if len(exists_line):
            cur.execute("DELETE FROM ignore_comments WHERE ignore_word = ? AND user_id = ?", (comment, user_id))