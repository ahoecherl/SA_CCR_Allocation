from enum import Enum
from itertools import zip_longest
from typing import List

import QuantLib as ql

from marketdata.EquitySpot import EquitySpot
from marketdata.util import today, calendar, day_count


class BlackVarianceSurfaceFactory():
    def __init__(self, optionMaturities: List[ql.Period], strikes: List[float], vols: List[List[float]]):
        self.optionMaturities = optionMaturities
        self.strikes = strikes
        self.vols = vols
        optionMaturityDates = []
        for optionMaturity in optionMaturities:
            optionMaturityDates.append(today + optionMaturity)
        self.optionMaturityDates = optionMaturityDates
        self.ql_BlackVarianceSurface = ql.BlackVarianceSurface(today,
                                                               calendar,
                                                               self.optionMaturityDates,
                                                               self.strikes,
                                                               list(map(list, zip_longest(*self.vols))),
                                                               # Black magic to transpose vols
                                                               day_count)
        self.ql_BlackVarianceSurface.enableExtrapolation()

    def __getitem__(self, optionMaturity: ql.Period) -> List[float]:
        optionMaturityIndex = self.optionMaturities.index(optionMaturity)
        return self.vols[optionMaturityIndex]

    def get_atm_shifted_surface_abs_one_pct(self, optionMaturity):
        bumpsize = 0.01
        optionMaturityIndex = self.optionMaturities.index(optionMaturity)
        shifted_vols = self.vols.copy()
        shifted_vols[optionMaturityIndex] = [v + bumpsize for v in shifted_vols[optionMaturityIndex]]
        result = ql.BlackVarianceSurface(today,
                                         calendar,
                                         self.optionMaturityDates,
                                         self.strikes,
                                         list(map(list, zip_longest(*shifted_vols))),
                                         # Black magic to transpose vols
                                         day_count)
        result.enableExtrapolation()
        return result


optionMaturities = [ql.Period(2, ql.Weeks),
                    ql.Period(1, ql.Months),
                    ql.Period(3, ql.Months),
                    ql.Period(6, ql.Months),
                    ql.Period(1, ql.Years),
                    ql.Period(2, ql.Years),
                    ql.Period(3, ql.Years),
                    ql.Period(5, ql.Years),
                    ql.Period(10, ql.Years),
                    ql.Period(15, ql.Years),
                    ql.Period(20, ql.Years),
                    ql.Period(30, ql.Years)]


class EquityVolatilityQuotes(Enum):
    ADS = BlackVarianceSurfaceFactory(optionMaturities, [EquitySpot.ADS.value.value() - 1,
                                                         EquitySpot.ADS.value.value(),
                                                         EquitySpot.ADS.value.value() + 1],
                                      [[0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2],
                                       [0.2, 0.2, 0.2]
                                       ])

    DBK = BlackVarianceSurfaceFactory(optionMaturities, [EquitySpot.DBK.value.value() - 1,
                                                         EquitySpot.DBK.value.value(),
                                                         EquitySpot.DBK.value.value() + 1],
                                      [[0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3],
                                       [0.3, 0.3, 0.3]
                                       ])


class EquityVolatility(Enum):
    ADS = ql.RelinkableBlackVolTermStructureHandle(
        EquityVolatilityQuotes.ADS.value.ql_BlackVarianceSurface
    )

    DBK = ql.RelinkableBlackVolTermStructureHandle(
        EquityVolatilityQuotes.DBK.value.ql_BlackVarianceSurface)
