from enum import Enum
import QuantLib as ql
from marketdata.util import today, calendar, day_count

class EquityVolatilty(Enum):
    ADS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, ql.QuoteHandle(ql.SimpleQuote(0.2)), day_count))
    DBK = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, ql.QuoteHandle(ql.SimpleQuote(0.3)), day_count))