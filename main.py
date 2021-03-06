import requests
import sqlite3
from PyQt5 import QtWidgets
import sys
import LaunchWindow


# API key stored in text file to keep it private from Github
def main():
    app = QtWidgets.QApplication(sys.argv)
    win = LaunchWindow.LaunchWindow()
    sys.exit(app.exec())


def get_key(prefix: str) -> str:
    with open(f'{prefix}secret.txt', 'r') as s:
        return s.readline()


def fetch_id(key: str, title: str):
    return requests.get(f"https://imdb-api.com/en/API/SearchTitle/{key}/{title}")


# There's a complicated compound statement here.
# It's basically unpacking json on the spot to find the ID of a series required to find it in the API
def fetch_series(key: str, title: str) -> dict:
    search = fetch_id(key, title)
    series = requests.get(f"https://imdb-api.com/en/API/Title/{key}/{search.json()['results'][0]['id']}/FullCast")
    return series.json()


# Use when the request will return a single record
def fetch_one(url: str, key: str, id: str) -> dict:
    search = requests.get(f"{url}/{key}/{id}")
    return search.json()


# Unpacks requests that may have multiple results
def fetch_many(url: str, key: str) -> dict:
    search = requests.get(f"{url}/{key}")
    json = parse_json(search.json())
    return json


# Deciphers JSON to return a 'cleaned' version for Python
def parse_json(data: dict) -> dict:
    clean = {}
    for i in range(1, len(data['items']) + 1):
        clean[i] = data['items'][i - 1]
    return clean


def output_to_file(data: dict):
    with open("titles.txt", 'a') as f:
        for v in data.values():
            f.write(str(v))
            f.write('\n')
            print(v)


def open_db(name: str) -> (sqlite3.Connection, sqlite3.Cursor):
    conn = sqlite3.connect(name)
    curs = conn.cursor()
    init_tables(curs)
    return conn, curs


def save_db(conn: sqlite3.Connection):
    conn.commit()


def close_db(conn: sqlite3.Connection):
    save_db(conn)
    conn.close()


# -----   TABLE CREATION METHODS ----- #
def init_tables(curs: sqlite3.Cursor):
    init_shows_table(curs)
    init_ratings_table(curs)
    init_movies_table(curs)
    init_popular_movies(curs)
    init_popular_shows(curs)


def init_shows_table(curs: sqlite3.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS shows
                    (imdbId TEXT PRIMARY KEY,
                     title TEXT NOT NULL,
                     fullTitle TEXT,
                     yr TEXT NOT NULL,
                     crew TEXT,
                     rating TEXT NOT NULL,
                     ratingCount TEXT NOT NULL);""")


def init_movies_table(curs: sqlite3.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS movies
                    (imdbId TEXT PRIMARY KEY,
                     title TEXT NOT NULL,
                     fullTitle TEXT,
                     yr TEXT NOT NULL,
                     crew TEXT,
                     rating TEXT NOT NULL,
                     ratingCount TEXT NOT NULL);""")


def init_popular_shows(curs: sqlite3.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS popularShows
                    (imdbId TEXT PRIMARY KEY,
                     rank TEXT,
                     rankUpDown TEXT DEFAULT 0,
                     title TEXT NOT NULL,
                     fullTitle TEXT,
                     yr TEXT NOT NULL,
                     crew TEXT,
                     rating TEXT NOT NULL,
                     ratingCount TEXT NOT NULL);""")


def init_popular_movies(curs: sqlite3.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS popularMovies
                    (imdbId TEXT PRIMARY KEY,
                     rank TEXT,
                     rankUpDown INTEGER DEFAULT 0,
                     title TEXT NOT NULL,
                     fullTitle TEXT,
                     yr TEXT NOT NULL,
                     crew TEXT,
                     rating TEXT NOT NULL,
                     ratingCount TEXT NOT NULL);""")


def init_ratings_table(curs: sqlite3.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS ratings
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     imdbId TEXT NOT NULL,
                     totalRating REAL NOT NULL,
                     totalVotes INTEGER NOT NULL,
                     ten_percent REAL NOT NULL DEFAULT 0,
                     ten_votes INTEGER NOT NULL DEFAULT 0,
                     nine_percent REAL NOT NULL DEFAULT 0,
                     nine_votes INTEGER NOT NULL DEFAULT 0,
                     eight_percent REAL NOT NULL DEFAULT 0,
                     eight_votes INTEGER NOT NULL DEFAULT 0,
                     seven_percent REAL NOT NULL DEFAULT 0,
                     seven_votes INTEGER NOT NULL DEFAULT 0,
                     six_percent REAL NOT NULL DEFAULT 0,
                     six_votes INTEGER NOT NULL DEFAULT 0,
                     five_percent REAL NOT NULL DEFAULT 0,
                     five_votes INTEGER NOT NULL DEFAULT 0,
                     four_percent REAL NOT NULL DEFAULT 0,
                     four_votes INTEGER NOT NULL DEFAULT 0,
                     three_percent REAL NOT NULL DEFAULT 0,
                     three_votes INTEGER NOT NULL DEFAULT 0,
                     two_percent REAL NOT NULL DEFAULT 0,
                     two_votes INTEGER NOT NULL DEFAULT 0,
                     one_percent REAL NOT NULL DEFAULT 0,
                     one_votes INTEGER NOT NULL DEFAULT 0,
                     FOREIGN KEY(imdbId) REFERENCES shows(imdbId));""")


# -----   RECORD CREATION METHODS ----- #
# Function expects a dict with dict objects as values.
# This is how the JSON is parsed, so it's easiest to work with like this.
def create_show_records(curs: sqlite3.Cursor, data: dict):
    for row in data.values():
        create_show_record(curs, row)


def create_show_record(curs: sqlite3.Cursor, row: dict):
    curs.execute("""INSERT INTO shows(imdbId, title, fullTitle, yr, crew, rating, ratingCount)
                            VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING""",
                 (row["imdbId"],
                  row["title"],
                  row["fullTitle"],
                  row["year"],
                  row["crew"],
                  row["imDbRating"],
                  row["imDbRatingCount"]))


def create_popular_show_records(curs: sqlite3.Cursor, data: dict):
    for row in data.values():
        create_popular_show_record(curs, row)


def create_popular_show_record(curs: sqlite3.Cursor, row: dict):
    curs.execute("""INSERT INTO popularShows(imdbId, rank, rankUpDown, title, fullTitle, yr, crew, rating, ratingCount)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING""",
                 (row["imdbId"],
                  row["rank"],
                  row["rankUpDown"],
                  row["title"],
                  row["fullTitle"],
                  row["year"],
                  row["crew"],
                  row["imDbRating"],
                  row["imDbRatingCount"]))


def create_popular_movie_records(curs: sqlite3.Cursor, data: dict):
    for row in data.values():
        create_popular_movie_record(curs, row)


def create_popular_movie_record(curs: sqlite3.Cursor, row: dict):
    curs.execute("""INSERT INTO popularMovies(imdbId, rank, rankUpDown, title, fullTitle, yr, crew, rating, ratingCount)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING""",
                 (row["imdbId"],
                  row["rank"],
                  int(row["rankUpDown"].replace(",", "")),
                  row["title"],
                  row["fullTitle"],
                  row["year"],
                  row["crew"],
                  row["imDbRating"],
                  row["imDbRatingCount"]))


def create_rating_records(curs: sqlite3.Cursor, table_name: str, data: dict):
    for row in data.values():
        create_rating_record(curs, table_name, row)


def create_rating_record(curs: sqlite3.Cursor, table_name: str, row: dict):
    curs.execute(f"""INSERT INTO {table_name}(imdbId, totalRating, totalVotes,
                                        ten_percent, ten_votes,
                                        nine_percent, nine_votes,
                                        eight_percent, eight_votes,
                                        seven_percent, seven_votes,
                                        six_percent, six_votes,
                                        five_percent, five_votes,
                                        four_percent, four_votes,
                                         three_percent, three_votes,
                                         two_percent, two_votes,
                                         one_percent, one_votes)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING""",
                 (row["imdbId"], row["title"], row["fullTitle"], row["ratings"][0]["percent"],
                  row["ratings"][0]["votes"], row["ratings"][1]["percent"], row["ratings"][1]["votes"],
                  row["ratings"][2]["percent"], row["ratings"][2]["votes"], row["ratings"][3]["percent"],
                  row["ratings"][3]["votes"], row["ratings"][4]["percent"], row["ratings"][4]["votes"],
                  row["ratings"][5]["percent"], row["ratings"][5]["votes"], row["ratings"][6]["percent"],
                  row["ratings"][6]["votes"], row["ratings"][7]["percent"], row["ratings"][7]["votes"],
                  row["ratings"][8]["percent"], row["ratings"][8]["votes"], row["ratings"][9]["percent"],
                  row["ratings"][9]["votes"]))


# -----   DATABASE MODIFICATION METHODS ----- #
# This function's SQL command doesn't properly sanitize inputs.
# I'm not sure how to allow input that works for different tables
# While also preventing SQL injection issues.
def update_record(curs: sqlite3.Cursor, table: str, data: dict):
    fields = package_fields_to_string(data)
    curs.execute(f"""UPDATE {table} SET {fields} WHERE imdbId = (?);""", [data["imdbId"]])


# Formats data to a SQL readable format. This would be done by hand, but the number and name of the
# fields varies by table. It also strips a trailing comma by slicing.
def package_fields_to_string(data: dict) -> str:
    request = ""
    for key in data.keys():
        request += key + " = \'" + data[key] + "\',"
    return request[:-1]


# It's assumed that the keys and values are already formatted to fit together.
# I get the keys using a SQL Pragma call, which gives a list of tuples. Index one is where the
# actual column name is stored in each tuple, hence why it's grabbed.
def package_fields_to_dict(keys: list[str], values: list[str]) -> dict:
    data_dict = {}
    for index in range(len(keys)):
        data_dict[keys[index][1]] = values[index]
    return data_dict


# id is passed as a tuple so the letters aren't interpreted as separate inputs.
def delete_record(curs: sqlite3.Cursor, table: str, id: str):
    curs.execute(f"""DELETE * FROM {table} WHERE imdbId == (?);""", (id, ))


# -----   DATABASE SEARCH METHODS ----- #
# Gets all information from a table and merges each record with columns into dicts for convenient use.
def query_entire_table(curs: sqlite3.Cursor, table_name: str) -> list[dict]:
    records = curs.execute(f"""SELECT * FROM {table_name};""").fetchall()
    keys = curs.execute(f"""PRAGMA table_info({table_name});""").fetchall()
    output = []
    for record in records:
        output.append(package_fields_to_dict(keys, record))
    return output


# ID is passed as a list, otherwise str is interpreted as a collection of 9 inputs.
# For clarity, that occurs because a string is also a collection, so the 9 inputs are characters.
def query_show(curs: sqlite3.Cursor, id: str):
    return curs.execute("""SELECT * FROM shows WHERE imdbId == (?)""", [id]).fetchall()


def query_popularity_changes(curs: sqlite3.Cursor, table_name: str, top: int, bottom: int):
    result = curs.execute(f"""SELECT * FROM {table_name} ORDER BY RankUpDown DESC LIMIT {top}""").fetchall()
    result.append(curs.execute(f"""SELECT * FROM {table_name} ORDER BY RankUpDown ASC LIMIT {bottom}""").fetchone())
    return result


def popular_movies_in_top(curs: sqlite3.Cursor):
    return curs.execute("""SELECT * FROM movies JOIN popularMovies 
                                ON movies.imdbId = popularMovies.imdbId""").fetchall()


def popular_shows_in_top(curs: sqlite3.Cursor):
    return curs.execute("""SELECT * FROM shows JOIN popularShows 
                                ON shows.imdbId = popularShows.imdbId""").fetchall()


# -----   DATA ANALYSIS METHODS ----- #
def total_shows_moving_up(curs: sqlite3.Cursor):
    result = curs.execute("""SELECT * FROM popularShows WHERE RankUpDown > 0""").fetchall()
    return len(result)


def total_shows_moving_down(curs: sqlite3.Cursor):
    result = curs.execute("""SELECT * FROM popularShows WHERE RankUpDown < 0""").fetchall()
    return len(result)


def total_movies_moving_up(curs: sqlite3.Cursor):
    result = curs.execute("""SELECT * FROM popularMovies WHERE RankUpDown > 0""").fetchall()
    return len(result)


def total_movies_moving_down(curs: sqlite3.Cursor):
    result = curs.execute("""SELECT * FROM popularMovies WHERE RankUpDown < 0""").fetchall()
    return len(result)


if __name__ == '__main__':
    main()
