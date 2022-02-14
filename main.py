import requests
import sqlite3


# API key stored in text file to keep it private from Github
def main():
    db = open_db("im.db")

    key = get_key("")

    data = fetch_top250(key)
    output_ratings(key, data)
    output_data(data)
    create_show_records(db[1], data)
    create_rating_records(db[1], data)
    close_db(db[0])


def get_key(prefix: str) -> str:
    with open(f'{prefix}secret.txt', 'r') as s:
        return s.readline()


def fetch_series(key: str, title: str) -> dict:
    search = requests.get(f"https://imdb-api.com/en/API/SearchTitle/{key}/{title}")
    series = requests.get(f"https://imdb-api.com/en/API/Title/{key}/{search.json()['results'][0]['id']}/FullCast")
    return series.json()


# I included a print statement here to illustrate an issue with the API.
# The total rating only appears as 0. The only useful information returned
# from a user rating API call is the spread of user votes on a 10-point scale
def fetch_user_rating(key: str, id: str) -> dict:
    rating = requests.get(f"https://imdb-api.com/en/API/UserRatings/{key}/{id}")
    print(rating.json())
    return rating.json()


def fetch_top250(key) -> dict:
    top = requests.get(f"https://imdb-api.com/en/api/Top250TVs/{key}")
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
    init_top_table(curs)
    init_ratings_table(curs)
    return conn, curs


def save_db(conn: sqlite3.Connection):
    conn.commit()


def close_db(conn: sqlite3.Connection):
    save_db(conn)
    conn.close()


def init_top_table(curs: sqlite3.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS shows
                    (imdbId TEXT PRIMARY KEY,
                     title TEXT NOT NULL,
                     fullTitle TEXT NOT NULL,
                     yr TEXT NOT NULL,
                     crew TEXT NOT NULL,
                     rating INTEGER NOT NULL,
                     ratingCount INTEGER NOT NULL);""")


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


def query_db(curs: sqlite3.Cursor, table: str, id: str):
    return curs.execute("""SELECT * FROM (?) WHERE imdbId == (?)""", (table, id))


if __name__ == '__main__':
    main()
