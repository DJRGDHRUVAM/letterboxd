
import mysql.connector
import movies_db  
import time
import os
import sys
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",  
    charset='utf8',
    database="padampoli"
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
    username VARCHAR(50),
    movie_title VARCHAR(255),
    rating FLOAT
)
""")




def clear_terminal():
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
        print("Registration successful")
        time.sleep(1.25)
        clear_terminal()
    except mysql.connector.IntegrityError:
        print("Username already exists.")
        time.sleep(1.25)
        clear_terminal()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"Login successful! Welcome {username}")
        time.sleep(2)
        clear_terminal()
        return username
    else:
        print("Invalid username or password.")
        time.sleep(2)
        clear_terminal()
        return None


def menu(username):
    while True:
        clear_terminal()
        print("--- MOVIE MENU ---")
        print("1. Display top 5 movies by rating")
        print("2. Rate a movie")
        print("3. Delete your rating")
        print("4. Show my ratings")
        print("5. Search movies")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            movies_db.display_top_movies()
        elif choice == "2":
            movies_db.rate_movie(username)
        elif choice == '3':
            movies_db.delete_rating(username)
        elif choice == "4":
            movies_db.show_my_ratings(username)
        elif choice == "5":
            movies_db.search_movies()
        elif choice == "6":
            print("Exiting to Login page...")
            time.sleep(1)
            clear_terminal()
            return
        else:
            print("Invalid choice.")
            time.sleep(2)
            clear_terminal()


def main():
    clear_terminal()
    while True:
        try:
            print("--- WELCOME TO PADAMPOLI THE BEST MOVIE RATING INTERFACE ---")
            print("a. Register")
            print("b. Login")
            print("c. Exit")
            choice = input("Enter choice: ")
            if choice.lower() == 'b':
                username = login()
                if username:
                    movies = movies_db.load_movies_from_csv("movies.csv")
                    movies_db.insert_movies(movies)
                    menu(username)
                    break
            elif choice.lower() == 'a':
                register()
            elif choice.lower() == 'c':
                print("Exiting...")
                time.sleep(1)
                clear_terminal()
                break
            else:
                print("Invalid choice.")
                time.sleep(2)
                clear_terminal()
        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
