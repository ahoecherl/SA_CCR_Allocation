from enum import Enum
import QuantLib as ql
from marketdata.util import today, calendar, day_count

Quotes = {'ADS': ql.SimpleQuote(0.2),
          'DBK': ql.SimpleQuote(0.3)}

class EquityVolatilty(Enum):
    ADS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, ql.QuoteHandle(Quotes['ADS']), day_count))
    DBK = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, ql.QuoteHandle(Quotes['DBK']), day_count))