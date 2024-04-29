import mysql.connector # "C:\ProgramData\Anaconda3\python.exe" -m pip install mysql-connector 
import json

db_conf = {
    "host":"localhost",
    "db_name": "predmet",
    "user":"root",
    "passwd":""
}

def get_DB_connection():
    mydb = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        passwd=db_conf["passwd"],
        database=db_conf["db_name"]
    )
    return mydb

def create_session():
    query = "INSERT INTO sessions (data) VALUES (%s)"
    values = (json.dumps({}),)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute(query, values)
    mydb.commit()
    return cursor.lastrowid 

def get_session(session_id):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id=" + str(session_id))
    myresult = cursor.fetchone()
    if myresult is None:
        return None, {}
    else:
        return myresult[0], json.loads(myresult[1])

def replace_session(session_id, data):#replace-prvo izbrisi, a onda ubaci (delete/insert)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("""
    REPLACE INTO sessions(session_id,data) 
    VALUES (%s,%s)""",
    (session_id, json.dumps(data)))
    mydb.commit()

def update_session(session_id, data):#replace-prvo izbrisi, a onda ubaci (delete/insert)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute('''
    UPDATE sessions SET data=%s 
    WHERE session_id=%s''', (json.dumps(data),session_id))   
    mydb.commit()

def destroy_session(session_id):
    mydb=get_DB_connection()
    cursor=mydb.cursor()
    query = 'DELETE FROM sessions WHERE session_id= (%s)'
    values = (session_id, )
    cursor.execute(query, values)
    mydb.commit()


########## FUNKCIJA ZA DODAVANJE PODATAKA U TABLICU USERS ########

def insert_user(ime,email,password_hash):
    mydb=get_DB_connection()
    cursor=mydb.cursor()
    query="INSERT INTO users (ime, email, password) VALUES (%s, %s, %s)"
    values=(ime,email,password_hash)
    cursor.execute(query,values)
    mydb.commit()


########## FUNKCIJE/QUERIJI ZA PROVJERU IMENA I EMAIL-A ##########

def chech_username_exists(ime):    
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE ime = %s", (ime,))
    return cursor.fetchone() is not None

def chech_email_exists(email):    
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone() is not None

################# FUNKCIJA ZA DOHVACANJE SIFRE #######

def get_password(ime):    
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT password FROM users WHERE ime = %s", (ime,))
    result = cursor.fetchone()
    return result[0] if result else None


############# FUNKCIJA ZA DOHVACANJE IMENA ############

def get_name(user_id):    
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT ime FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

############ FUNKCIJA ZA DOHVACANJE ID-A ##############

def get_user_id(username):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT id FROM users WHERE ime = %s", (username,))
    result = cursor.fetchone()
    return result[0] if result else None


####### UPDATE PASSWORD ########

def update_password(user_id, new_password):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    query = "UPDATE users SET password = %s WHERE id = %s"
    values = (new_password, user_id)
    cursor.execute(query, values)
    mydb.commit()