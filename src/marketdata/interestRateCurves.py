import QuantLib as ql
from marketdata.util import today, day_count
from enum import Enum

flat_ois_quote = ql.SimpleQuote(0.01)
flat_ois_quote_handle = ql.QuoteHandle(flat_ois_quote)

ois_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, flat_ois_quote_handle, day_count))
libor_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, flat_ois_quote_handle, day_count))

class InterestRateCurve(Enum):
    USDLIBOR3M = libor_curve_handle
    EONIA = ois_curve_handle