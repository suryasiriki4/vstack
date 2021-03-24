import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question text, answer text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM questions")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, question, answer):
        self.cur.execute("INSERT INTO questions VALUES (NULL, ?, ?)", question, answer)
        self.conn.commit()
    