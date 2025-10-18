import mysql.connector
import csv
import time 

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    charset="utf8"
)
database.autocommit = True
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    year INT,
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
                "age_limit": row["age_limit"].lower(),
                "genre": row["genre"].lower(),
                "language": row["language"].lower()   # <-- added
            })
    return movies



def insert_movies(movies):
    cursor.execute("SELECT * FROM movies")
    if len(cursor.fetchall()) == 0:
        for movie in movies:
            cursor.execute("""
                INSERT INTO movies (title, year, age_limit, genre, language)
                VALUES (%s, %s, %s, %s, %s)
            """, (movie["title"], movie["year"],
                  movie["age_limit"], movie["genre"], movie["language"]))
        database.commit()


def get_all_movies():
    cursor.execute("SELECT title, year, age_limit, genre FROM movies")
    return cursor.fetchall()

def display_top_movies():
    # --- Valid options ---
    valid_genres = ["thriller", "action", "scifi", "romance", "fantasy", "any"]
    valid_ages = ["g", "pg", "pg13", "r", "any"]
    valid_languages = ["english", "malayalam", "tamil", "telugu", "hindi", "any"]

    # --- User inputs ---
    while True:
        genre = input("Enter genre [Thriller, Action, SciFi, Romance, Fantasy or 'any']: ").lower()
        if genre in valid_genres:
            break
        print("Invalid genre. Try again.")

    while True:
        age = input("Enter age category [G, PG, PG13, R or 'any']: ").lower()
        if age in valid_ages:
            break
        print("Invalid age category. Try again.")

    while True:
        language = input("Enter language [English, Malayalam, Tamil, Telugu, Hindi or 'any']: ").lower()
        if language in valid_languages:
            break
        print("Invalid language. Try again.")

    # --- Get global mean rating (C) and count threshold (m) ---
    cursor.execute("SELECT AVG(rating), COUNT(DISTINCT movie_title) FROM ratings")
    result = cursor.fetchone()
    C = result[0] if result[0] else 0
    m = 5  # Minimum number of ratings required to count toward weighted average

    # --- Build query dynamically ---
    query = f"""
    SELECT 
        m.title,
        m.year,
        m.genre,
        m.age_limit,
        m.language,
        COUNT(r.rating) AS num_ratings,
        AVG(r.rating) AS avg_rating,
        ((COUNT(r.rating) / (COUNT(r.rating) + {m})) * AVG(r.rating) +
         ({m} / (COUNT(r.rating) + {m})) * {C}) AS weighted_avg
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
    ORDER BY weighted_avg DESC
    LIMIT 5
    """

    cursor.execute(query, tuple(params))
    top_movies = cursor.fetchall()

    if top_movies:
        print("\n🏆 Top 5 Movies (Weighted Avg):")
        for m in top_movies:
            num = m[5]
            avg = round(m[6], 2) if m[6] else "—"
            wavg = round(m[7], 2) if m[7] else "—"
            print(f"{m[0].title()} ({m[1]}) | Genre: {m[2].title()} | Age: {m[3].upper()} | "
                  f"Lang: {m[4].title()} | Ratings: {num} | Avg: {avg} | Weighted: {wavg}")
        input("\nPress Enter to return to menu...")
    else:
        print("No movies found with the selected filters.")
        time.sleep(2)



def rate_movie(username):
    search_title = input("Enter movie title to rate: ").strip()
    
    cursor.execute("SELECT title FROM movies WHERE LOWER(title) LIKE %s", (f"%{search_title.lower()}%",))
    matches = cursor.fetchall()
    
    if not matches:
        print("Your movie does not exist.")
        adding = input("Want to add? (y/n): ").lower()
        if adding == 'y':
            add_movies(search_title)
            movie_title = search_title  # ✅ define it after adding
        else:
            return None
    
    elif len(matches) == 1:
        movie_title = matches[0][0]
    else:
        print("Multiple movies found:")
        for i, m in enumerate(matches, 1):
            print(f"{i}. {m[0]}")
        while True:
            choice = input(f"Enter the number of the movie you want to rate (1-{len(matches)}): ")
            if choice.isdigit() and 1 <= int(choice) <= len(matches):
                movie_title = matches[int(choice) - 1][0]
                break
            else:
                print("Invalid choice, try again.")
    
    # Ask rating safely
    while True:
        try:
            rating = int(input("Rate this movie (1-10): "))
            if 1 <= rating <= 10:
                break
            print("Rating must be 1–10.")
        except ValueError:
            print("Enter a valid integer.")
    
    cursor.execute("INSERT INTO ratings (username, movie_title, rating) VALUES (%s, %s, %s)",
                   (username, movie_title, rating))
    database.commit()
    print("✅ Rating saved!")
    time.sleep(2)


def add_movies(movie_title):
    year = int(input("Enter the year of the movie: "))

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
        "INSERT INTO movies (title, year,age_limit, genre, language) VALUES (%s, %s, %s, %s, %s)",
        (movie_title, year, age, genre, language)
    )
    database.commit()
    print("✅ Movie added successfully!")
    with open('movies.csv', 'a+', newline='', encoding='utf-8') as file:
        csv_w = csv.writer(file)
        csv_w.writerow([movie_title, year, age, genre, language])
    time.sleep(2)




def delete_rating(username):
    # Ask which movie rating to delete
    movie_title = input("Enter the title of the movie rating you want to delete: ")
    
    # Check if the rating exists
    cursor.execute("SELECT * FROM ratings WHERE username = %s AND movie_title = %s", (username, movie_title))
    data = cursor.fetchall()
    
    if not data:
        print("❌ You have not rated this movie yet.")
        time.sleep(2)
        return
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete your rating for '{movie_title}'? (y/n): ").lower()
    if confirm != 'y':
        print("⚠️ Deletion canceled.")
        time.sleep(2)
        return
    
    # Delete rating
    cursor.execute("DELETE FROM ratings WHERE username = %s AND movie_title = %s", (username, movie_title))
    database.commit()
    print("✅ Your rating has been deleted successfully!")
    time.sleep(2)


def show_my_ratings(username):
    # Fetch all ratings by this user
    cursor.execute("""
        SELECT r.movie_title, r.rating, m.genre, m.age_limit, m.language
        FROM ratings r
        JOIN movies m ON r.movie_title = m.title
        WHERE r.username = %s
        ORDER BY r.movie_title
    """, (username,))
    
    user_ratings = cursor.fetchall()
    
    if not user_ratings:
        print("❌ You haven't rated any movies yet.")
        time.sleep(2)
        return
    
    print("\n🎬 Your Rated Movies:")
    for movie in user_ratings:
        print(f"{movie[0].title()} | Rating: {movie[1]} | Genre: {movie[2].title()} | Age: {movie[3].upper()} | Language: {movie[4].title()}")
    input("\nPress Enter to return to menu...")


def search_movies():
    search_term = input("Enter a part of the movie title to search: ").strip().lower()
    if not search_term:
        print("❌ Search term cannot be empty.")
        time.sleep(2)
        return

    # Search movies and calculate average rating
    cursor.execute("""
        SELECT 
            m.title, 
            m.year, 
            m.genre, 
            m.age_limit, 
            m.language, 
            AVG(r.rating) AS avg_rating
        FROM movies m
        LEFT JOIN ratings r ON m.title = r.movie_title
        WHERE LOWER(m.title) LIKE %s
        GROUP BY m.title, m.year, m.genre, m.age_limit, m.language
        ORDER BY avg_rating DESC
        LIMIT 20
    """, (f"%{search_term}%",))

    results = cursor.fetchall()
    
    if not results:
        print(f"❌ No movies found matching '{search_term}'.")
        time.sleep(2)
        return

    print(f"\n🎬 Movies matching '{search_term}': (showing up to 20 results)")
    for idx, m in enumerate(results, start=1):
        avg_rating = round(m[5], 1) if m[5] else "No ratings yet"
        print(f"{idx:02d}. {m[0].title()} ({m[1]}) | Genre: {m[2].title()} | "
              f"Age: {m[3].upper()} | Language: {m[4].title()} | Avg Rating: {avg_rating}")

    input("\nPress Enter to return to menu...")

