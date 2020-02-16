import QuantLib as ql
from marketdata import InterestRateCurves

euribor_3M_index = ql.Euribor3M(InterestRateCurves.libor_curve_handle)
libor_3M_index = ql.USDLibor(ql.Period(3, ql.Months), InterestRateCurves.libor_curve_handle)