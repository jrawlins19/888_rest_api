import os
import sys
import pytest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src"))
from selection import Selection


@pytest.fixture
def test_selection():
    return Selection("Test", "test", 0.5, True, "Win")


def test_get_name(test_selection):
    assert "Bonza" == test_selection.get_name()
