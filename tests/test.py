import main
import pytest


@pytest.fixture
def test_top():
    top = main.fetch_top250(main.get_key())
    assert len(top) == 250



