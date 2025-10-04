import mysql.connector
import csv
import time 

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="postboxd",
    charset="utf8"
)
database.autocommit = True
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    year INT,
    rating FLOAT,
    age_limit VARCHAR(10),
    genre VARCHAR(50),
    language VARCHAR(50)
)
""")



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


def insert_movies(movies):
    cursor.execute("SELECT * FROM movies")
    if len(cursor.fetchall()) == 0:
        for movie in movies:
            cursor.execute("""
                INSERT INTO movies (title, year, rating, age_limit, genre, language)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (movie["title"], movie["year"], movie["rating"],
                  movie["age_limit"], movie["genre"], movie["language"]))
        database.commit()


def get_all_movies():
    cursor.execute("SELECT title, year, rating, age_limit, genre FROM movies")
    return cursor.fetchall()

def display_top_movies():
    # --- Valid options ---
    valid_genres = ["thriller", "action", "scifi", "romance", "fantasy", "any"]
    valid_ages = ["g", "pg", "pg13", "r", "any"]
    valid_languages = ["english", "malayalam", "tamil", "telugu", "hindi", "any"]

    # --- User inputs with validation ---
    while True:
        genre = input("Enter genre [Thriller, Action, SciFi, Romance, Fantasy or 'any']: ").lower()
        if genre in valid_genres:
            break
        print("❌ Invalid genre. Try again.")

    while True:
        age = input("Enter age category [G, PG, PG13, R or 'any']: ").lower()
        if age in valid_ages:
            break
        print("❌ Invalid age category. Try again.")

    while True:
        language = input("Enter language [English, Malayalam, Tamil, Telugu, Hindi or 'any']: ").lower()
        if language in valid_languages:
            break
        print("❌ Invalid language. Try again.")

    # --- Build query dynamically ---
    query = """
    SELECT 
        m.title, m.year, m.genre, m.age_limit, m.language, AVG(r.rating) AS avg_rating
    FROM movies m
    LEFT JOIN ratings r ON m.title = r.movie_title
    """
    params = []
    filters = []

    if genre != "any":
        filters.append("m.genre = %s")
        params.append(genre)
    if age != "any":
        filters.append("m.age_limit = %s")
        params.append(age)
    if language != "any":
        filters.append("m.language = %s")
        params.append(language)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += """
    GROUP BY m.title, m.year, m.genre, m.age_limit, m.language
    ORDER BY avg_rating DESC
    LIMIT 5
    """

    # --- Execute and display ---
    cursor.execute(query, tuple(params))
    top_movies = cursor.fetchall()

    if top_movies:
        print("\n🏆 Top 5 Movies:")
        for m in top_movies:
            avg_rating = round(m[5], 1) if m[5] else "No ratings yet"
            print(f"{m[0]} ({m[1]}) | Genre: {m[2]} | Age: {m[3]} | Language: {m[4]} | Avg Rating: {avg_rating}")
        input("\nPress Enter to return to menu...")
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
    
def add_movies(movie_title):
    year = int(input("Enter the year of the movie: "))
    imdb = float(input("Enter IMDb rating of the movie (0-10): "))

    # --- Genre validation ---
    valid_genres = ["thriller", "action", "scifi", "romance", "fantasy"]
    while True:
        genre = input("Enter genre [Thriller, Action, SciFi, Romance, Fantasy]: ").lower()
        if genre in valid_genres:
            break
        print("❌ Invalid genre. Try again.")

    # --- Age validation ---
    valid_ages = ["g", "pg", "pg13", "r"]
    while True:
        age = input("Enter age category [G, PG, PG13, R]: ").lower()
        if age in valid_ages:
            break
        print("❌ Invalid age category. Try again.")

    # --- Language validation ---
    valid_languages = ["english", "malayalam", "tamil", "telugu", "hindi"]
    while True:
        language = input("Enter language [English, Malayalam, Tamil, Telugu, Hindi]: ").lower()
        if language in valid_languages:
            break
        print("❌ Invalid language. Try again.")

    cursor.execute(
        "INSERT INTO movies (title, year, rating, age_limit, genre, language) VALUES (%s, %s, %s, %s, %s, %s)",
        (movie_title, year, imdb, age, genre, language)
    )
    database.commit()
    print("✅ Movie added successfully!")
