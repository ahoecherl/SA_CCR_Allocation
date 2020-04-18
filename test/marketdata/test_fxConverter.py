import pytest

from marketdata.fxConverter import fxConvert
from marketdata.fx_spot import FxSpot
from utilities.Enums import Currency


def test_oneWay():
    fxspot = FxSpot.EURUSD.value
    eur = 10
    usd = fxspot*eur
    assert usd == fxConvert(Currency.EUR, Currency.USD, eur)