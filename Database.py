import sqlite3


class User():

    def __init__(self, email="", first="", password=""):
        self.email = email
        self.first = first
        self.password = password
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()

    def add(self):
        self.cursor.execute(f"""
        INSERT INTO people VALUES
        ('{self.email}', '{self.first}', '{self.password}')
        """)
        self.connection.commit()

    def getData(self, email):
        self.cursor.execute(f"""
        SELECT * FROM people
        WHERE email = '{email}'
        """)
        results = self.cursor.fetchone()
        self.email = email
        self.first = results[1]
        self.password = results[2]


connection = sqlite3.connect('mydata.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
    email TEXT PRIMARY KEY,
    first_name TEXT,
    password TEXT
    )
""")

def makeUser(email, first_name, password):
    try:
        user = User(email, first_name, password)
        user.add()
        return first_name
    except sqlite3.IntegrityError:
        return 'failed'
    except:
        return 'failed'

    connection.commit()


def findUser(email, get='all'):
    try:
        user = User()
        user.getData(email)
        if get == 'all':
            return user.email, user.first, user.password
        else:
            return user.first

    except:
        return 'failed'


connection.close()