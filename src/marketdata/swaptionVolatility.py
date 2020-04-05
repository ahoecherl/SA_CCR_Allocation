import QuantLib as ql
from marketdata.util import business_day_convention, calendar, day_count
from enum import Enum

optionTenors = [ql.Period(1, ql.Months),
                ql.Period(3, ql.Months),
                ql.Period(6, ql.Months),
                ql.Period(1, ql.Years),
                ql.Period(2, ql.Years)]
swapTenors = [ql.Period(1, ql.Months),
              ql.Period(2, ql.Months),
              ql.Period(3, ql.Months),
              ql.Period(20, ql.Years)]
vols = [[ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1)],
        [ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1)],
        [ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1)],
        [ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1)],
        [ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1),
         ql.SimpleQuote(0.1)],
        ]

def createHandle(vols):
    result = []
    for row in vols:
        nested = []
        result.append(nested)
        for cell in row:
            nested.append(ql.QuoteHandle(cell))
    return result

def parallelshift(vols, bumpsize: float):
    for row in vols:
        for cell in row:
            cell.setValue(cell.value()+bumpsize)

class SwaptionVolatility(Enum):
    EONIA = ql.SwaptionVolatilityMatrix(calendar, business_day_convention, optionTenors, swapTenors, createHandle(vols), day_count)
    USDLIBOR3M = ql.SwaptionVolatilityMatrix(calendar, business_day_convention, optionTenors, swapTenors, createHandle(vols), day_count)
    EURIBOR3M = ql.SwaptionVolatilityMatrix(calendar, business_day_convention, optionTenors, swapTenors, createHandle(vols), day_count)
