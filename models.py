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
                "email"	TEXT DEFAULT NULL UNIQUE,
                "real_name" TEXT DEFAULT NULL, 
                "date_created" TEXT DEFAULT (DATETIME('now', 'localtime')),
                "logo_url" TEXT DEFAULT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
                );""")
    cur.execute("""
                CREATE TABLE "posts" (
                    "id"	INTEGER NOT NULL,
                    "text"	TEXT DEFAULT NULL,
                    "content"	TEXT DEFAULT NULL,
                    "date"	TEXT DEFAULT (DATETIME('now', 'localtime')),
                    "user_id"	INTEGER,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("user_id") REFERENCES "users"("id")
                );
                """)
    cur.execute("""
                CREATE TABLE "post_likes"(
                    "user_id" INTEGER NOT NULL,
                    "post_id" INTEGER NOT NULL,
                    "date_liked" TEXT DEFAULT(DATETIME('now', 'localtime')),
                    PRIMARY KEY("user_id", "post_id"),
                    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
                    FOREIGN KEY("post_id") REFERENCES "posts"("id") ON DELETE CASCADE
                );
                """)
class Users():
    def __init__(self, name, password,
                 email = "NULL", id = 0,
                 real_name = "NULL", date_created ="NULL",
                 logo_url = "NULL"):
        self.id = id
        self.name = name
        self.real_name= real_name
        self.password = password
        self.date_created = date_created
        self.email = email
        self.logo_url = logo_url
        
class Posts():
    def __init__(self,user_id, id = 0, text = None, image = None, date = None):
        self.id = id
        self.user_id = user_id
        self.text = text
        self.image = image
        self.date = date
        
def create_user(user: Users):
    db = connect_to_db()
    cur = db.cursor()
    query = f"INSERT INTO users(name, password_hashed) VALUES ('{user.name}', '{user.password}')"
    cur.execute(query)
    db.commit()
    db.close()

def find_user_by_name(name):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users WHERE name='{name}'")
    result = cur.fetchone()
    db.close()
    if result is None:
        return False
    return Users(id = result[0], name = result[1], password=result[2])

def find_user_by_email(email):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users WHERE email='{email}'")
    result = cur.fetchone()
    db.close()
    if result is None or result == False:
        return False

    return Users(*result)

def create_post(id = None,text = None, image = None):
    db = connect_to_db()
    cur = db.cursor()
    query = f"INSERT INTO posts(user_id, text, content) VALUES (?, ?, ?)"
    cur.execute(query, (id, text, image))
    db.commit()
    db.close()

def find_all_posts():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM posts")
    result = cur.fetchall()
    db.close()
    posts = list()
    for r in result:
        posts.append(Posts(
            id = r[0],
            text = r[1],
            image = r[2],
            date= r[3],
            user_id= r[4]
        ))
    return posts  