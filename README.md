
# 🎬 Padampoli Movie Rating System

A simple **Python + MySQL** movie rating system that allows users to register, log in, rate movies, and view top-rated films using a **weighted average algorithm** (inspired by IMDb’s formula).

---

## 🚀 Features

✅ **User Management**

* Register and log in with unique usernames
* Store user data securely in MySQL

✅ **Movie Database**

* Loads movies from a CSV file on first run
* Users can add new movies with validated details (genre, language, age rating, etc.)

✅ **Ratings System**

* Rate any movie from **1–10**
* Update or delete your ratings anytime
* Shows your personal rated movie list

✅ **Smart Rankings**

* View top 5 movies with **weighted average ratings**
  Formula:
  [
  WR = \frac{v}{v+m} \times R + \frac{m}{v+m} \times C
  ]
  where

  * **R** = average rating for the movie
  * **v** = number of votes for the movie
  * **m** = minimum votes required (default = 5)
  * **C** = global mean rating across all movies

✅ **Search Functionality**

* Find movies by title
* Displays both **average** and **weighted** ratings

---

## 🧩 Tech Stack

| Component    | Technology                       |
| ------------ | -------------------------------- |
| Language     | Python 3                         |
| Database     | MySQL                            |
| File Storage | CSV (for initial movie data)     |
| Libraries    | `mysql.connector`, `csv`, `time` |

---

## 🛠️ Installation & Setup

### 1️⃣ Install MySQL

Make sure you have **MySQL Server** running locally.

Example command to start MySQL (Linux/macOS):

```bash
sudo service mysql start
```

### 2️⃣ Create the Database

You don’t need to manually create one —
the script automatically creates a database named **`padampoli`** and required tables on startup.

### 3️⃣ Configure MySQL Credentials

Open your Python file and edit:

```python
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",  # <--- change this if needed
    database="padampoli"
)
```

### 4️⃣ Add Initial Movie Data

Place a CSV file named **`movies.csv`** in the same folder.
Example format:

```csv
title,year,age_limit,genre,language
Inception,2010,pg13,scifi,english
Interstellar,2014,pg13,scifi,english
The Dark Knight,2008,pg13,action,english
Vikram,2022,r,action,tamil
KGF Chapter 2,2022,pg13,action,kannada
```

### 5️⃣ Run the Program

```bash
python main.py
```

---

## 📖 How to Use

### 🧍‍♂️ For Users:

1. **Register or Log in**
2. Choose from the main menu:

   * 🎥 **Browse or Search Movies**
   * ⭐ **Rate Movies**
   * 🏆 **View Top Movies**
   * 🗑️ **Delete a Rating**
   * 👤 **View Your Rated Movies**
3. Exit safely — your data stays saved in MySQL.

---

## 🧮 Weighted Average Example

If a movie “Inception” has:

* R = 8.5 (average rating)
* v = 10 votes
  and
* C = 7.2 (global average)
* m = 5 (minimum threshold)

then:
[
WR = \frac{10}{10+5} × 8.5 + \frac{5}{10+5} × 7.2 = 8.06
]

---

## 📂 Project Structure

```
padampoli/
│
├── login.py                # user registration and login system
├── movies_db.py            # movie + rating logic (this file)
├── movies.csv              # initial movie list
├── README.md               # this file
└── requirements.txt        # (optional) for dependencies
```

---

## Authors

**Devika**
**Neha**
**Tuvya**
**Druv**

---

## 🪪 License

This project is open-source and free to use under the **MIT License**.

---
