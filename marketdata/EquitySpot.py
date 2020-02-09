from enum import Enum
import QuantLib as ql

class EquitySpot(Enum):
    ADS = ql.QuoteHandle(ql.SimpleQuote(42))
    DBK = ql.QuoteHandle(ql.SimpleQuote(9))