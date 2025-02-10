import sqlite3


def get_db_connection():
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_user_table():
    try:
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("""
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            username TEXT NOT NULL UNIQUE,
            gmail TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email_verified BOOLEAN DEFAULT FALSE);""")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def create_quests_table():
    try: 
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("""
            CREATE TABLE IF NOT EXISTS quests (
            quest_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT NOT NULL UNIQUE,
            points INTEGER NOT NULL,
            description TEXT NOT NULL UNIQUE,
            time TIME);""")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def create_profile_table():
    try: 
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("""
            CREATE TABLE IF NOT EXISTS profile (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            user_id INTEGER NOT NULL UNIQUE,
            photo TEXT NOT NULL,
            prof_description TEXT NOT NULL,
            points INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE);""")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def create_tables():
    create_user_table()
    create_quests_table()
    create_profile_table()
