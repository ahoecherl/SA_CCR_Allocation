import QuantLib as ql
from typing import List


abs_bump = 0.0001
rel_bump = 0.0025

def fd_simple_quotes(quotes: List[ql.SimpleQuote], instrument ):
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

def dv01_abs_one_bp(quotes: List[ql.SimpleQuote], instrument  ):
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

def dv01_rel_one_percent(quotes: List[ql.SimpleQuote], instrument):
    p0 = instrument.get_price()
    origVals = []
    for quote in quotes:
        origVals.append(quote.value())
        quote.setValue(quote.value()*(1+rel_bump))
    p1 = instrument.get_price()
    multiplier = 0.01 / rel_bump
    dv01pct = (p1 - p0) * multiplier
    origVals.reverse()
    for quote in quotes:
        quote.setValue(origVals.pop())
    return dv01pct