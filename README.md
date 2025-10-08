# 🎬 Padampoli Movie Rating System

A **command-line Python application** with MySQL integration that allows users to:

- 🔑 Register and log in  
- 🎞️ Load movies from a CSV file into MySQL  
- ⭐ Rate movies (with update support)  
- 🗑️ Delete their ratings  
- 👀 View their own ratings  
- 🔍 Search and filter movies by genre, age rating, and language  

---

## ⚙️ Features

- **User Authentication**  
  Users can register and log in (stored securely in MySQL).

- **Movies Database**  
  Movies are loaded from `movies.csv` into a MySQL database (`padampoli.movies`).  
  Users can also add new movies interactively.

- **Ratings System**  
  Users can rate movies (1–10). Ratings are stored in the `ratings` table.  
  Duplicate ratings are avoided — updating is supported.

- **Search and Filters**  
  - Top 5 movies by average rating (with genre, age, and language filters)  
  - Search movies by title  
  - Show user’s own ratings  

---
