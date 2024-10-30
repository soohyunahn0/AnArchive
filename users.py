from connection import get_db
from passlib.hash import pbkdf2_sha256 as pw
from user import create_profile

def create_table():
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''CREATE TABLE if not exists users (
        "userId" INTEGER primary key autoincrement,
        "username" Text,
        "password" Text
    ) ''')

def create_account(username, password):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('select * from users where username = ?', [username])
    rows = result.fetchall()
    row_count = len(rows)
    if row_count > 0 :
        return "Can't create account, user already exists"
    else:
        hashed = pw.hash(password)
        sql.execute('''insert into users
        (username, password) values
        (?, ?)''', [username, hashed])
        connection.commit()
        create_profile(sql.lastrowid)
        return "Account created, you can login now"

def check_account(username, password):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('''select * from users
                            where username = ?''', [username])
    data = result.fetchone()
    if data:
        hashed = data['password']
        check_hash = pw.verify(password, hashed)
        if check_hash:
            return data['userId']
    else:
        return False
