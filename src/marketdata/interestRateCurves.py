import QuantLib as ql
from marketdata.util import today, day_count
from enum import Enum

ois_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, day_count))
libor_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.02, day_count))

class InterestRateCurve(Enum):
    USDLIBOR3M = libor_curve_handle
    EONIA = ois_curve_handle