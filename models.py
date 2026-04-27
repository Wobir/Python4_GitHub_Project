import sqlite3 as sql

def connect_to_db():
    return sql.connect("instance/db.db")

def check_db():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users';",
    )
    if cur.fetchone() is None:
        init_db()
    db.close()

def init_db():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("""
                CREATE TABLE "users" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT NOT NULL UNIQUE,
                "password_hashed"	TEXT NOT NULL,
                "email"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("id" AUTOINCREMENT)
                );""")
    cur.execute("""
                CREATE TABLE "posts" (
                    "id"	INTEGER NOT NULL,
                    "text"	TEXT,
                    "content"	TEXT,
                    "date"	INTEGER,
                    "user_id"	INTEGER,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("user_id") REFERENCES "users"("id")
                );
                """)
class Users():
    def __init__(self, name, password, email, id = 0):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        
class Posts():
    def __init__(self,user_id, id = 0, text = None, content = None, date = None):
        self.id = id
        self.user_id = user_id
        self.text = text
        self.content = content
        self.date = date
        
def create_user(user: Users):
    db = connect_to_db()
    cur = db.cursor()
    query = f"INSERT INTO users(name, password_hashed, email) VALUES ('{user.name}', '{user.password}', '{user.email}')"
    cur.execute(query)
    db.commit()
    db.close()

def find_user_by_name(name):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users WHERE name='{name}'")
    result = cur.fetchone()
    db.close()
    if result is None or result == False:
        return False
    return Users(*result)

def find_user_by_email(email):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users WHERE email='{email}'")
    result = cur.fetchone()
    db.close()
    if result is None or result == False:
        return False

    return Users(*result)
    