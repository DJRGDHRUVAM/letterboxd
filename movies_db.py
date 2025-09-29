import mysql.connector
import csv
import time 

# Connect to MySQL
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="postboxd",
    charset="utf8"
)
database.autocommit = True
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
    cursor.execute('select * from movies')
    store = cursor.fetchall()
    if len(store) == 0:  
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

def display_top_movies():
    genre = input("Enter genre \n [Thriller, Action, SciFi, Romance, Fantasy or 'any']: ").lower()
    age = input("Enter age category (or 'any'): ").lower()
    language = input("Enter language (or 'any'): ").lower()

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
            time.sleep(1)
    else:
        print("No movies found with the selected filters.")
        time.sleep(2)

def rate_movie(username):
    movie_title = input("Enter movie title to rate: ")
    cursor.execute("SELECT * FROM movies WHERE title = %s", (movie_title,))
    data = cursor.fetchall()
    if len(data) == 0:
        print("Your movie does not exist")
        adding = input("Want to add? (y/n): ").lower()
        if adding=='y':
            add_movies(movie_title)
        else:
            None
    while True:
        try:
            rating = int(input("Rate this movie (1-10): "))
            if 1 <= rating <= 10:
                break
            else:
                print("Rating must be 1–10.")
                time.sleep(2)
        except ValueError:
            print("Enter a valid number.")
            time.sleep(2)
    cursor.execute("INSERT INTO ratings (username, movie_title, rating) VALUES (%s, %s, %s)",
                   (username, movie_title, rating))
    database.commit()
    print("✅ Rating saved!")
    time.sleep(2)
    
def add_movies(movie):
    year = int(input("Enter the year of movie: "))
    imdb = float(input("Enter the imdb rating of movie: "))
    genre = input("Enter genre \n [Thriller, Action, SciFi, Romance, Fantasy or ']: ").lower()
    age = input("Enter age category : ").lower()
    language = input("Enter language : ").lower()
    cursor.execute(
    "INSERT INTO movies (title, year, rating, age_limit, genre, language) VALUES (%s, %s, %s, %s, %s, %s)",
    (movie, year, imdb, age, genre, language))
