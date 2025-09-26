import mysql.connector

database = mysql.connector.connect(host="localhost", user="root",password="mysql",)
cursor = database.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS postboxd")
cursor.execute("USE postboxd")
database.autocommit = True

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")




def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        print("Registration successful")
    except:
        print("Username already exists.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"Login successful! Welcome {username}")
        return True
    else:
        print("Invalid username or password.")
        return False

def main():
    while True:
        print("\n LOGIN SYSTEM")
        print("a. Login")
        print("b. Register")
        print("c. Exit")
        choice = input("Enter choice: ")

        if choice.lower() == 'a':
            if login():
                #Continue to the main application
                break
        elif choice.lower() == 'b':
            register()
        elif choice.lower() == 'c':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

main()