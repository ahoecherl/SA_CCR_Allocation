import QuantLib as ql
from marketdata import interestRateCurves_old
from enum import Enum

euribor_3M_index = ql.Euribor3M(interestRateCurves_old.libor_curve_handle)
euribor_3M_index.addFixing(ql.Date(8, ql.May, 2019), 0.01)
libor_3M_index = ql.USDLibor(ql.Period(3, ql.Months), interestRateCurves_old.libor_curve_handle)
libor_3M_index.addFixing(ql.Date(8, ql.May, 2019), 0.02)

class InterestRateIndex(Enum):
    EURIBOR3M = euribor_3M_index
    USDLIBOR3M = libor_3M_index