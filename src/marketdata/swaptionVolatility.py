import QuantLib as ql
from enum import Enum

from instruments.interestRateInstrument.interestRateDerivativeConventions import IRSConventions, SwaptionConventions
from utilities.Enums import Currency

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
            cell.setValue(cell.value() + bumpsize)


class SwaptionVolatility(Enum):
    EUR = ql.SwaptionVolatilityStructureHandle(
        ql.SwaptionVolatilityMatrix(SwaptionConventions.EUR.value['Calendar'],
                                    SwaptionConventions.EUR.value['DateRoll'],
                                    optionTenors, swapTenors, createHandle(vols),
                                    SwaptionConventions.EUR.value['DayCount']))

    USD = ql.SwaptionVolatilityStructureHandle(
        ql.SwaptionVolatilityMatrix(SwaptionConventions.USD.value['Calendar'],
                                    SwaptionConventions.USD.value['DateRoll'],
                                    optionTenors, swapTenors, createHandle(vols),
                                    SwaptionConventions.USD.value['DayCount']))
