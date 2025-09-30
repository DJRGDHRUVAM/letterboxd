import mysql.connector
import movies_db  
import time
import os
import sys
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",  
    database="postboxd",
    charset='utf8'
)
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    movie_title VARCHAR(255),
    rating INT
)
""")

cursor.execute("SHOW COLUMNS FROM movies LIKE 'language'")
if cursor.fetchone() is None:
    cursor.execute("ALTER TABLE movies ADD COLUMN language VARCHAR(50) DEFAULT 'English'")
    database.commit()



def clear_terminal():
    """Clears the terminal screen based on the operating system."""
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        database.commit()
        print("✅ Registration successful")
        time.sleep(1.25)
        clear_terminal()
    except mysql.connector.IntegrityError:
        print("❌ Username already exists.")
        time.sleep(1.25)
        clear_terminal()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"✅ Login successful! Welcome {username}")
        time.sleep(2)
        clear_terminal()
        return username
    else:
        print("❌ Invalid username or password.")
        time.sleep(2)
        clear_terminal()
        return None


def menu(username):
    while True:
        clear_terminal() 
        print("\n--- MOVIE MENU ---")
        print("1. Display top 5 movies by rating")
        print("2. Rate a movie")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            movies_db.display_top_movies()
        elif choice == "2":
            movies_db.rate_movie(username)
        elif choice == "3":
            print("Exiting menu...")
            break
        else:
            print("Invalid choice.")
            time.sleep(2)

def main():
    while True:
        print("\n--- LOGIN SYSTEM ---")
        print("a. Login")
        print("b. Register")
        print("c. Exit")
        choice = input("Enter choice: ")

        if choice.lower() == 'a':
            username = login()
            if username:
                movies = movies_db.load_movies_from_csv("movies.csv")
                movies_db.insert_movies(movies)
                menu(username)
                break
        elif choice.lower() == 'b':
            register()
        elif choice.lower() == 'c':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
            time.sleep(2)

if __name__ == "__main__":
    main()
