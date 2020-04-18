import QuantLib as ql
from typing import List

from instruments.Trade import Trade

abs_bump = 0.0001

def fd_simple_quotes(quotes: List[ql.SimpleQuote], instrument : Trade):
    p0 = instrument.get_price()
    origVals = []
    for quote in quotes:
        origVals.append(quote.value())
        quote.setValue(quote.value()+abs_bump)
    p1 = instrument.get_price()
    finite_difference = (p1-p0)/abs_bump
    origVals.reverse()
    for quote in quotes:
        quote.setValue(origVals.pop())
    return finite_difference

def dv01_abs_one_bp(quotes: List[ql.SimpleQuote], instrument : Trade ):
    p0 = instrument.get_price()
    origVals = []
    for quote in quotes:
        origVals.append(quote.value())
        quote.setValue(quote.value() + abs_bump)
    p1 = instrument.get_price()
    multiplier = 0.0001 / abs_bump
    dv01 = (p1 - p0) * multiplier
    origVals.reverse()
    for quote in quotes:
        quote.setValue(origVals.pop())
    return dv01