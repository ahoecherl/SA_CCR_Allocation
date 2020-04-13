from typing import List, Tuple

import QuantLib as ql
from enum import Enum

from instruments.interestRateInstrument.interestRateDerivativeConventions import IRSConventions, SwaptionConventions
from utilities.Enums import Currency


class SwaptionVolatilitySurface():
    def __init__(self, optionTenors: List[ql.Period], swapTenors: List[ql.Period], vols: List[List[ql.SimpleQuote]]):
        self.optionTenors = optionTenors
        self.swapTenors = swapTenors
        self.vols = vols

    def __getitem__(self, keytuple : Tuple[ql.Period, ql.Period]) -> ql.SimpleQuote:
        """

        :param keytuple: First item of tuple is option tenor, second is swap tenor
        :return:
        """
        optionTenor = keytuple[0]
        swapTenor = keytuple[1]
        optionIndex = self.optionTenors.index(optionTenor)
        swapIndex = self.swapTenors.index(swapTenor)
        return self.vols[optionIndex][swapIndex]


optionTenors = [ql.Period(1, ql.Months),
                ql.Period(3, ql.Months),
                ql.Period(6, ql.Months),
                ql.Period(1, ql.Years),
                ql.Period(2, ql.Years)]
swapTenors = [ql.Period(1, ql.Years),
              ql.Period(2, ql.Years),
              ql.Period(5, ql.Years),
              ql.Period(10, ql.Years),
              ql.Period(15, ql.Years),
              ql.Period(20, ql.Years),
              ql.Period(30, ql.Years)]


class SwaptionVolatilityQuotes(Enum):
    USD = SwaptionVolatilitySurface(optionTenors, swapTenors,
                                    [[ql.SimpleQuote(0.725840071), ql.SimpleQuote(0.858671188), ql.SimpleQuote(0.992712814), ql.SimpleQuote(1.030566502), ql.SimpleQuote(0.993208446), ql.SimpleQuote(0.992187047), ql.SimpleQuote(1.036687799)],
                                    [ql.SimpleQuote(1.129603264), ql.SimpleQuote(1.062651791), ql.SimpleQuote(1.032570638), ql.SimpleQuote(1.038675641), ql.SimpleQuote(0.971190742), ql.SimpleQuote(0.954252243), ql.SimpleQuote(0.977101955)],
                                    [ql.SimpleQuote(1.038788819), ql.SimpleQuote(0.95160501), ql.SimpleQuote(0.982859451), ql.SimpleQuote(0.976081629), ql.SimpleQuote(0.905274503), ql.SimpleQuote(0.887375492), ql.SimpleQuote(0.90154807)],
                                    [ql.SimpleQuote(1.024089943), ql.SimpleQuote(1.03217673), ql.SimpleQuote(0.949286522), ql.SimpleQuote(0.921671557), ql.SimpleQuote(0.859068799), ql.SimpleQuote(0.845229901), ql.SimpleQuote(0.859595692)],
                                    [ql.SimpleQuote(1.139743663), ql.SimpleQuote(1.030655798), ql.SimpleQuote(0.900676861), ql.SimpleQuote(0.862388515), ql.SimpleQuote(0.811886583), ql.SimpleQuote(0.796711329), ql.SimpleQuote(0.808801882)]
                                    ])

    EUR = SwaptionVolatilitySurface(optionTenors, swapTenors,
                                    [[ql.SimpleQuote(0.004063812), ql.SimpleQuote(0.004051285), ql.SimpleQuote(0.005530748), ql.SimpleQuote(0.007411004), ql.SimpleQuote(0.007967218), ql.SimpleQuote(0.008345463), ql.SimpleQuote(0.008900338)],
                                    [ql.SimpleQuote(0.003923772), ql.SimpleQuote(0.004017309), ql.SimpleQuote(0.005444917), ql.SimpleQuote(0.00730743), ql.SimpleQuote(0.007674986), ql.SimpleQuote(0.007926001), ql.SimpleQuote(0.008293852)],
                                    [ql.SimpleQuote(0.003580317), ql.SimpleQuote(0.003749496), ql.SimpleQuote(0.005377688), ql.SimpleQuote(0.006968861), ql.SimpleQuote(0.007204294), ql.SimpleQuote(0.007392478), ql.SimpleQuote(0.007641038)],
                                    [ql.SimpleQuote(0.003597136), ql.SimpleQuote(0.004134255), ql.SimpleQuote(0.005488724), ql.SimpleQuote(0.00673724), ql.SimpleQuote(0.006909312), ql.SimpleQuote(0.007064848), ql.SimpleQuote(0.007250501)],
                                    [ql.SimpleQuote(0.004827405), ql.SimpleQuote(0.005106651), ql.SimpleQuote(0.005877155), ql.SimpleQuote(0.006649729), ql.SimpleQuote(0.006698853), ql.SimpleQuote(0.006737146), ql.SimpleQuote(0.006789876)]
                                    ])


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
                                    SwaptionVolatilityQuotes.EUR.value.optionTenors,
                                    SwaptionVolatilityQuotes.EUR.value.swapTenors,
                                    createHandle(SwaptionVolatilityQuotes.EUR.value.vols),
                                    SwaptionConventions.EUR.value['DayCount'],
                                    False,
                                    ql.Normal
                                    ))

    USD = ql.SwaptionVolatilityStructureHandle(
        ql.SwaptionVolatilityMatrix(SwaptionConventions.USD.value['Calendar'],
                                    SwaptionConventions.USD.value['DateRoll'],
                                    SwaptionVolatilityQuotes.USD.value.optionTenors,
                                    SwaptionVolatilityQuotes.USD.value.swapTenors,
                                    createHandle(SwaptionVolatilityQuotes.USD.value.vols),
                                    SwaptionConventions.USD.value['DayCount'],
                                    False,
                                    ql.ShiftedLognormal))
