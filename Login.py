import mysql.connector
import movies_db  # Make sure movies_db.py exists

# --- Connect to MySQL ---
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",  # your MySQL password
    database="postboxd",
    charset='utf8'
)
cursor = database.cursor()

# --- Create users table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")

# --- Create ratings table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    movie_title VARCHAR(255),
    rating INT
)
""")

# --- Ensure 'language' column exists in movies ---
cursor.execute("SHOW COLUMNS FROM movies LIKE 'language'")
if cursor.fetchone() is None:
    cursor.execute("ALTER TABLE movies ADD COLUMN language VARCHAR(50) DEFAULT 'English'")
    database.commit()

# --- Register ---
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        database.commit()
        print("✅ Registration successful")
    except mysql.connector.IntegrityError:
        print("❌ Username already exists.")

# --- Login ---
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"✅ Login successful! Welcome {username}")
        return username
    else:
        print("❌ Invalid username or password.")
        return None

# --- Rate a movie ---
def rate_movie(username):
    movie_title = input("Enter movie title to rate: ")
    while True:
        try:
            rating = int(input("Rate this movie (1-10): "))
            if 1 <= rating <= 10:
                break
            else:
                print("Rating must be 1–10.")
        except ValueError:
            print("Enter a valid number.")
    cursor.execute("INSERT INTO ratings (username, movie_title, rating) VALUES (%s, %s, %s)",
                   (username, movie_title, rating))
    database.commit()
    print("✅ Rating saved!")

# --- Display top 5 movies ---
def display_top_movies():
    genre = input("Enter genre (or 'any'): ")
    age = input("Enter age category (or 'any'): ")
    language = input("Enter language (or 'any'): ")

    query = """
    SELECT m.title, m.year, m.genre, m.age_limit, m.language, AVG(r.rating) as avg_rating
    FROM movies m
    LEFT JOIN ratings r ON m.title = r.movie_title
    WHERE 1=1
    """
    params = []

    if genre.lower() != "any":
        query += " AND m.genre = %s"
        params.append(genre)
    if age.lower() != "any":
        query += " AND m.age_limit = %s"
        params.append(age)
    if language.lower() != "any":
        query += " AND m.language = %s"
        params.append(language)

    query += " GROUP BY m.title ORDER BY avg_rating DESC LIMIT 5"

    cursor.execute(query, tuple(params))
    top_movies = cursor.fetchall()

    if top_movies:
        print("\n🏆 Top 5 Movies:")
        for m in top_movies:
            avg_rating = round(m[5], 1) if m[5] else "No ratings yet"
            print(f"{m[0]} ({m[1]}) | Genre: {m[2]} | Age: {m[3]} | Language: {m[4]} | Avg Rating: {avg_rating}")
    else:
        print("No movies found with the selected filters.")

# --- Menu ---
def menu(username):
    while True:
        print("\n--- MOVIE MENU ---")
        print("1. Display top 5 movies by rating")
        print("2. Rate a movie")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            display_top_movies()
        elif choice == "2":
            rate_movie(username)
        elif choice == "3":
            print("Exiting menu...")
            break
        else:
            print("Invalid choice.")

# --- Main ---
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
                # Load movies CSV once after first login
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

if __name__ == "__main__":
    main()
