import main
import pytest


def test_top():
    top = main.fetch_top250(main.get_key("../"))
    assert len(top) == 250


def test_db():
    key = main.get_key("../")
    db = main.open_db("sample.db")
    db[1].execute("""DROP TABLE IF EXISTS shows""")
    db[1].execute("""DROP TABLE IF EXISTS ratings""")
    wheel = main.fetch_series(key, "The Wheel of Time")
    print(wheel)
    main.create_show_record(db[1], wheel)
    main.create_rating_record(db[1], main.fetch_user_rating(key, wheel["id"]))
    main.save_db(db[0])
    print(main.query_db(db[1], "shows", wheel["id"]))
