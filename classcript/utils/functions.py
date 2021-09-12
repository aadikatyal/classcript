import os
import hashlib

def get_database_connection():
    import sqlite3
    sqlite_file = 'notes.db'
    file_exists = os.path.isfile(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    if not file_exists:
        create_sqlite_tables(conn)
    return conn

def create_sqlite_tables(conn):
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()

def get_user_count():
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False

def check_user_exists(username, password):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False

def store_last_login(user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login=(strftime('%m-%d-%Y', 'now', 'localtime')) WHERE id=?", (user_id, ))
        conn.commit()
        cursor.close()
    except:
        cursor.close()

def check_username(username):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username, ))
        if cursor.fetchone():
            return True
    except:
        return False

def signup_user(username, password, email):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def get_user_data(user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (str(user_id), ))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def get_data_using_user_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def get_data_using_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()

def get_number_of_notes(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(note) FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()

def get_data():
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes')
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()

def add_note(note_title, note, note_markdown, user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(note_title, note, note_markdown, user_id) VALUES (?, ?, ?, ?)", (note_title, note, note_markdown, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def edit_note(note_title, note, note_markdown, note_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET note_title=?, note=?, note_markdown=? WHERE id=?", (note_title, note, note_markdown, note_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def delete_note_using_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def generate_password_hash(password):
    hashed_value = hashlib.md5(password.encode())
    return hashed_value.hexdigest()

def get_search_data(pattern, user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE user_id=? AND note LIKE ? LIMIT 3", (user_id, '%' + pattern + '%'))
        results = cursor.fetchall()
        results = [(results[i][0], results[i][3]) for i in range(len(results))]
        cursor.close()
        return results
    except:
        cursor.close()

def get_rest_data_using_user_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        fieldnames = [f[0] for f in cursor.description]
        cursor.close()
        if len(results) == 0:
            return None
        else:
            outer = {}
            for i in range(len(results)):
                data = {}
                for j in range(len(results[0])):
                    data[fieldnames[j]] = results[i][j]
                outer[int(i)] = data

            return outer
    except:
        cursor.close()