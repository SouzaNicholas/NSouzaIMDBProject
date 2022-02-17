import requests
import sqlite3


# API key stored in text file to keep it private from Github
def main():
    key = get_key("")

    data = fetch_many("https://imdb-api.com/en/API/MostPopularTVs", key)
    output_data(data)


def get_key(prefix: str) -> str:
    with open(f'{prefix}secret.txt', 'r') as s:
        return s.readline()


def fetch_series(key: str, title: str) -> dict:
    search = requests.get(f"https://imdb-api.com/en/API/SearchTitle/{key}/{title}")
    series = requests.get(f"https://imdb-api.com/en/API/Title/{key}/{search.json()['results'][0]['id']}/FullCast")
    return series.json()


def fetch_user_rating(key: str, id: str) -> dict:
    rating = requests.get(f"https://imdb-api.com/en/API/UserRatings/{key}/{id}")
    return rating.json()


def fetch_many(url, key) -> dict:
    top = requests.get(f"{url}/{key}")
    json = parse_json(top.json())
    return json


# Deciphers JSON to return a 'cleaned' version for Python
def parse_json(data_dict: dict) -> dict:
    clean = {}
    for i in range(1, len(data_dict['items']) + 1):
        clean[i] = data_dict['items'][i - 1]
    return clean


# Was going to use f strings for file writing, but it caused issues with the dict keys
# being in quotation marks
def output_ratings(key, data_dict):
    with open("titles.txt", 'w') as f:
        WoT = fetch_series(key, "The Wheel of Time")['results'][0]
        f.write(WoT["title"] + " - Rating: " + fetch_user_rating(key, WoT["id"])["totalRating"] + '\n')
        f.write(data_dict[1]["title"] + " - Rating: " +
                fetch_user_rating(key, data_dict[1]["id"])["totalRating"] + '\n')
        f.write(data_dict[50]["title"] + " - Rating: " +
                fetch_user_rating(key, data_dict[50]["id"])["totalRating"] + '\n')
        f.write(data_dict[100]["title"] + " - Rating: " +
                fetch_user_rating(key, data_dict[100]["id"])["totalRating"] + '\n')
        f.write(data_dict[200]["title"] + " - Rating: " +
                fetch_user_rating(key, data_dict[200]["id"])["totalRating"] + '\n')


def output_data(data_dict):
    with open("titles.txt", 'a') as f:
        for v in data_dict.values():
            f.write(str(v))
            f.write('\n')
            print(v)


def open_db(name: str) -> (sqlite3.Connection, sqlite3.Cursor):
    conn = sqlite3.connect(name)
    curs = conn.cursor()
    init_shows_table(curs)
    init_ratings_table(curs)
    return conn, curs


def save_db(conn: sqlite3.Connection):
    conn.commit()


def close_db(conn: sqlite3.Connection):
    save_db(conn)
    conn.close()


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
                     rankUpDown TEXT DEFAULT 0,
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


# Function expects a dict with dict objects as values.
# This is how the JSON is parsed, so it's easiest to work with like this.
def create_show_records(curs: sqlite3.Cursor, data: dict):
    for row in data.values():
        create_show_record(curs, row)


def create_show_record(curs: sqlite3.Cursor, row: dict):
    curs.execute("""INSERT INTO shows(imdbId, title, fullTitle, yr, crew, rating, ratingCount)
                            VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING""",
                 (row["id"],
                  row["title"],
                  row["fullTitle"],
                  row["year"],
                  row["crew"],
                  row["imDbRating"],
                  row["imDbRatingCount"]))


def create_rating_records(curs: sqlite3.Cursor, data: dict):
    for row in data.values():
        create_rating_record(curs, row)


def create_rating_record(curs: sqlite3.Cursor, row: dict):
    curs.execute("""INSERT INTO ratings(imdbId, totalRating, totalVotes,
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
                 (row["imDbId"], row["title"], row["fullTitle"], row["ratings"][0]["percent"],
                  row["ratings"][0]["votes"], row["ratings"][1]["percent"], row["ratings"][1]["votes"],
                  row["ratings"][2]["percent"], row["ratings"][2]["votes"], row["ratings"][3]["percent"],
                  row["ratings"][3]["votes"], row["ratings"][4]["percent"], row["ratings"][4]["votes"],
                  row["ratings"][5]["percent"], row["ratings"][5]["votes"], row["ratings"][6]["percent"],
                  row["ratings"][6]["votes"], row["ratings"][7]["percent"], row["ratings"][7]["votes"],
                  row["ratings"][8]["percent"], row["ratings"][8]["votes"], row["ratings"][9]["percent"],
                  row["ratings"][9]["votes"]))


# ID is passed as a list, otherwise str is interpreted as a collection of 9 inputs.
def query_db(curs: sqlite3.Cursor, id: str):
    return curs.execute("""SELECT * FROM shows WHERE imdbId == (?)""", [id]).fetchall()


if __name__ == '__main__':
    main()
