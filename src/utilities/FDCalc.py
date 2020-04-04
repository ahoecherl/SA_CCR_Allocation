import QuantLib as ql
from typing import List

abs_bump = 0.0001

def fd_simple_quotes(quotes: List[ql.SimpleQuote], instrument):
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