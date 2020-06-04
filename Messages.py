import sqlite3

class Message():
    def __init__(self, name="", pin=''):
        self.pin=pin
        self.name=name
        self.connection = sqlite3.connect("mydata.db", check_same_thread = False)
        self.cursor = connection.cursor()

    def new(self):
        cursor.execute(f"""
        INSERT INTO chats VALUES 
        ('{self.name}', '{self.pin}')
        """)

    def find(self, name):
        self.cursor.execute(f"""
        SELECT * FROM chats
        WHERE chat_name = '{name}'
        """)
        results = self.cursor.fetchone()
        self.name = name
        self.pin = results[1]

connection = sqlite3.connect("mydata.db", check_same_thread = False)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
    chat_name TEXT PRIMARY KEY,
    chat_pin TEXT
    )
""")


def new(name, pin):
    try:
        obj = Message(name, pin)
        obj.new()
        connection.commit()
        return "made new!"
    except:
        return "failed"

def find(name):
    try:
        a=Message()
        a.find(name)
        return [a.name, a.pin]
    except:
        return "failed"

cursor.execute("""
    CREATE TABLE IF NOT EXISTS message_data (
    t TEXT,
    f TEXT,
    content TEXT
    )
""")

def newMessage(t, f, content):
    cursor.execute(f"""
    INSERT INTO message_data VALUES 
    ('{t}', '{f}', '{content}')
    """)
    connection.commit()
    return "made new!"


def findMessages(t):
    cursor.execute(f"""
            SELECT * FROM message_data
            WHERE t = '{t}'
            """)
    a = cursor.fetchall()
    return a

findMessages('Alex')

