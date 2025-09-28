import mysql.connector
import csv

# --- Connect to MySQL ---
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    charset="utf8"
)
cursor = database.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS postboxd")
database.commit()
cursor.execute("USE postboxd")

# --- Create movies table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    year INT,
    rating FLOAT DEFAULT 0,
    age_limit VARCHAR(10),
    genre VARCHAR(50),
    language VARCHAR(50) DEFAULT 'English'
)
""")
database.commit()

# --- Load movies from CSV ---
def load_movies_from_csv(file_path="movies.csv"):
    movies = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append({
                "title": row.get("title", "Unknown"),
                "year": int(row.get("year", 0)),
                "rating": float(row.get("rating", 0)),
                "age_limit": row.get("age_limit", "N/A"),
                "genre": row.get("genre", "N/A"),
                "language": row.get("language", "English")
            })
    return movies

# --- Insert movies into DB safely ---
def insert_movies(movies):
    for movie in movies:
        cursor.execute("""
            INSERT INTO movies (title, year, rating, age_limit, genre, language)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            movie["title"],
            movie["year"],
            movie["rating"],
            movie["age_limit"],
            movie["genre"],
            movie["language"]
        ))
    database.commit()

# --- Fetch all movies ---
def get_all_movies():
    cursor.execute("SELECT title, year, rating, age_limit, genre, language FROM movies")
    return cursor.fetchall()
