import main
import pytest


@pytest.fixture
def test_top():
    top = main.fetch_top250(main.get_key("../"))
    assert len(top) == 250


def test_db():
    db = main.open_db("sample.db")
    db[1].execute("""DROP TABLE IF EXISTS shows""")
    db[1].execute("""DROP TABLE IF EXISTS ratings""")
    main.init_top_table(db[1])
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
