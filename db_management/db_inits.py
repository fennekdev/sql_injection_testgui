import os
import sqlite3


def standart_db_init(db_name,standart_data=None):
    if standart_data is None:
        standart_data = [("Bob","bob123"),
                         ("Tom","supersecure123"),
                         ("Fridulin","password"),
                         ("Nico","snuslove69"),
                         ("Karim","qwertzuiop"),
                         ("Moneyboy","moneyyy420"),
                         ("admin","youwillneverguessthispassword")]
    if not os.path.exists(db_name):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
            );
        """)

        
        cursor.executemany(f"INSERT INTO users (username,password) VALUES (?,?)",(standart_data))
        connection.commit()
        connection.close()