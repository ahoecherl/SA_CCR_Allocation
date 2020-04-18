import pytest
from marketdata.util import today

def test_today():
    assert "%4d-%02d-%02d" % (today.year(), today.month(), today.dayOfMonth()) == '2019-05-10'