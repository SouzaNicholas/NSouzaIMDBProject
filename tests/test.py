import main
import pytest


@pytest.fixture
def test_fixture():
    assert 0


def test_top():
    top = main.fetch_many("https://imdb-api.com/en/API/Top250TVs", main.get_key("../"))
    assert len(top) == 250


def test_db():
    db = main.open_db("sample.db")
    db[1].execute("""DROP TABLE IF EXISTS shows""")
    db[1].execute("""DROP TABLE IF EXISTS ratings""")
    main.init_shows_table(db[1])
    main.init_ratings_table(db[1])
    sample_data = {
        "Seinfeld": {"id": "tt0000000", "title": "Seinfeld", "fullTitle": "Seinfeld(1989)",
                     "year": "1989", "crew": "Jerry Seinfeld", "imDbRating": "9.5", "imDbRatingCount": "1000000"},
        "The Room": {"id": "tt0000001", "title": "The Room", "fullTitle": "The Room(2003)",
                     "year": "2003", "crew": "Tommy Wiseau", "imDbRating": "3.2", "imDbRatingCount": "20000"},
        "Stop Making Sense": {"id": "tt0000002", "title": "Stop Making Sense", "fullTitle": "Stop Making Sense(1984)",
                              "year": "1984", "crew": "David Byrne", "imDbRating": "8.6", "imDbRatingCount": "523692"}
    }
    main.create_show_records(db[1], sample_data)
    main.save_db(db[0])
    record = list(main.query_db(db[1], sample_data["The Room"]["id"])[0])
    assert list(sample_data["The Room"].values()) == record
    main.close_db(db[0])


def test_movie_delta():
    db = main.open_db("sample.db")
    db[1].execute("""DROP TABLE IF EXISTS popularMovies""")
    main.init_popular_movies(db[1])
    key = main.get_key("../")
    data = main.fetch_many("https://imdb-api.com/en/API/MostPopularMovies", key)
    main.create_popular_movie_records(db[1], data)

    sample_data = [
        ('tt1798632', '64', 3755, 'Firestarter', 'Firestarter (2022)', '2022', 'Keith Thomas (dir.), Zac Efron, Ryan Kiera Armstrong', '', '0'),
        ('tt10131024', '49', 1452, 'Shut In', 'Shut In (2022)', '2022', 'D.J. Caruso (dir.), Rainey Qualley, Jake Horowitz', '6.9', '3165'),
        ('tt7740496', '1', 0, 'Nightmare Alley', 'Nightmare Alley (2021)', '2021', 'Guillermo del Toro (dir.), Bradley Cooper, Cate Blanchett', '7.2', '54942'),
        ('tt14039582', '27', 109, 'Drive My Car', 'Drive My Car (2021)', '2021', 'Ryûsuke Hamaguchi (dir.), Hidetoshi Nishijima, Tôko Miura', '7.8', '12077')
    ]

    assert sample_data != main.query_movie_delta(db[1])
