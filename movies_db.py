import mysql.connector
import csv

# Connect to MySQL
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="postboxd",
    charset="utf8"
)
cursor = database.cursor()

# Create movies table
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    year INT,
    rating FLOAT,
    age_limit VARCHAR(10),
    genre VARCHAR(50)
)
""")

# --- Load movies from CSV ---
def load_movies_from_csv(file_path="movies.csv"):
    movies = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append({
                "title": row["title"],
                "year": int(row["year"]),
                "rating": float(row["rating"]),
                "age_limit": row["age_limit"],
                "genre": row["genre"]
            })
    return movies

# --- Insert movies into DB ---
def insert_movies(movies):
    for movie in movies:
        cursor.execute("""
            INSERT INTO movies (title, year, rating, age_limit, genre)
            VALUES (%s, %s, %s, %s, %s)
        """, (movie["title"], movie["year"], movie["rating"], movie["age_limit"], movie["genre"]))
    database.commit()

# --- Fetch all movies ---
def get_all_movies():
    cursor.execute("SELECT title, year, rating, age_limit, genre FROM movies")
    return cursor.fetchall()
