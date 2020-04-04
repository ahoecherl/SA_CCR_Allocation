from enum import Enum
import QuantLib as ql

Quotes = {'ADS': ql.SimpleQuote(42),
          'DBK': ql.SimpleQuote(9)}

class EquitySpot(Enum):
    ADS = ql.QuoteHandle(Quotes['ADS'])
    DBK = ql.QuoteHandle(Quotes['DBK'])
