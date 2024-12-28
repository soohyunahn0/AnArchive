from connection import get_db

def setup_profile():
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''CREATE TABLE if not exists profile
    (
        "UserId" INTEGER,
        "FirstName" Text,
        "LastName" Text,
        "Email" Text,
        "Bio" Text,
        foreign key(UserId) references users(UserId)
    )''')

def create_profile(user_id):
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''insert into profile (UserId, FirstName,
         LastName, Email, Bio, ProfileImage) values(?,?,?,?,?) ''', 
         [user_id, "Famous", "Panda", "panda@xyz.com", "Something about a panda"])
    connection.commit()

def update_profile(user_id, first_name, last_name, email, bio):
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''update profile set FirstName = ?,
                   LastName = ?, Email = ?, Bio = ?
                   where userId = ?''', 
                [first_name, last_name, email, bio, user_id])
    connection.commit()

def get_profile(user_id):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('''select *, users.username 
                            from profile
                            join users using(userId)
                            where userId = ?''', [user_id])
    return result.fetchone()