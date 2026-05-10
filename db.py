import sqlite3

def save_to_db(topic, content):
    conn = sqlite3.connect("database.db")
    
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            content TEXT
        )
    """)
    
    cursor.execute(
        "INSERT INTO results (topic, content) VALUES (?, ?)",
        (topic, content)
    )
    
    conn.commit()
    conn.close()

