import QuantLib as ql
from marketdata.util import today, day_count

ois_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, day_count))
libor_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.02, day_count))