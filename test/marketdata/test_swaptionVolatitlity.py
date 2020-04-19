import pytest
import QuantLib as ql

from marketdata.swaptionVolatility import SwaptionVolatility, SwaptionVolatilitySurface


def test_turnIntoNormal():
    vols = SwaptionVolatility.USD
    asdf =1

def test_turnIntoShiftedVolas():
    pass


def test_SwaptionVolatilitySurface():
    optionTenors = [ql.Period(2, ql.Weeks),
                    ql.Period(1, ql.Months),
                    ql.Period(3, ql.Months),
                    ql.Period(6, ql.Months),
                    ql.Period(2, ql.Years)]
    swapTenors = [ql.Period(1, ql.Months),
                  ql.Period(2, ql.Months),
                  ql.Period(3, ql.Months),
                  ql.Period(20, ql.Years)]
    vols = [[ql.SimpleQuote(0.1),
             ql.SimpleQuote(0.2),
             ql.SimpleQuote(0.3),
             ql.SimpleQuote(0.4)],
            [ql.SimpleQuote(0.5),
             ql.SimpleQuote(0.6),
             ql.SimpleQuote(0.7),
             ql.SimpleQuote(0.8)],
            [ql.SimpleQuote(0.9),
             ql.SimpleQuote(1.0),
             ql.SimpleQuote(1.1),
             ql.SimpleQuote(1.2)],
            [ql.SimpleQuote(1.3),
             ql.SimpleQuote(1.4),
             ql.SimpleQuote(1.5),
             ql.SimpleQuote(1.6)],
            [ql.SimpleQuote(1.7),
             ql.SimpleQuote(1.8),
             ql.SimpleQuote(1.9),
             ql.SimpleQuote(2.0)],
            ]

    testSurface = SwaptionVolatilitySurface(optionTenors, swapTenors, vols)
    assert testSurface[(ql.Period(2, ql.Weeks), ql.Period(2, ql.Months))].value() == ql.SimpleQuote(0.2).value()

    testSurface[ql.Period(2, ql.Weeks)]
    asdf = 1