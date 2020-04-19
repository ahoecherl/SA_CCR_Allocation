from enum import Enum
import QuantLib as ql

class EquitySpotQuote(Enum):
    ADS = ql.SimpleQuote(42)
    DBK = ql.SimpleQuote(9)

class EquitySpot(Enum):
    ADS = ql.QuoteHandle(EquitySpotQuote['ADS'].value)
    DBK = ql.QuoteHandle(EquitySpotQuote['DBK'].value)
