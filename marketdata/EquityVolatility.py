from enum import Enum
from QuantLib import *
from marketdata.util import today, calendar, day_count

class EquityVolatilty(Enum):
    ADS = BlackVolTermStructureHandle(BlackConstantVol(today, calendar, QuoteHandle(SimpleQuote(0.2)), day_count))
    DBK = BlackVolTermStructureHandle(BlackConstantVol(today, calendar, QuoteHandle(SimpleQuote(0.3)), day_count))