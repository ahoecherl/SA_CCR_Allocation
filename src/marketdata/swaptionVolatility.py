import QuantLib as ql
from marketdata.util import business_day_convention, calendar, day_count
from enum import Enum

optionTenors = [ql.Period(1, ql.Months),
                ql.Period(3, ql.Months),
                ql.Period(6, ql.Months),
                ql.Period(1, ql.Years),
                ql.Period(2, ql.Years)]
swapTenors = [ql.Period(1, ql.Months),
              ql.Period(2, ql.Months),
              ql.Period(3, ql.Months),
              ql.Period(20, ql.Years)]
vols = [[ql.QuoteHandle(ql.SimpleQuote(0.2)),
         ql.QuoteHandle(ql.SimpleQuote(0.2)),
         ql.QuoteHandle(ql.SimpleQuote(0.2)),
         ql.QuoteHandle(ql.SimpleQuote(0.2))],
        [ql.QuoteHandle(ql.SimpleQuote(0.3)),
         ql.QuoteHandle(ql.SimpleQuote(0.3)),
         ql.QuoteHandle(ql.SimpleQuote(0.3)),
         ql.QuoteHandle(ql.SimpleQuote(0.3))],
        [ql.QuoteHandle(ql.SimpleQuote(0.4)),
         ql.QuoteHandle(ql.SimpleQuote(0.4)),
         ql.QuoteHandle(ql.SimpleQuote(0.4)),
         ql.QuoteHandle(ql.SimpleQuote(0.4))],
        [ql.QuoteHandle(ql.SimpleQuote(0.5)),
         ql.QuoteHandle(ql.SimpleQuote(0.5)),
         ql.QuoteHandle(ql.SimpleQuote(0.5)),
         ql.QuoteHandle(ql.SimpleQuote(0.5))],
        [ql.QuoteHandle(ql.SimpleQuote(0.6)),
         ql.QuoteHandle(ql.SimpleQuote(0.6)),
         ql.QuoteHandle(ql.SimpleQuote(0.6)),
         ql.QuoteHandle(ql.SimpleQuote(0.6))],
        ]

class SwaptionVolatility(Enum):
    EONIA =  ql.SwaptionVolatilityMatrix(calendar, business_day_convention, optionTenors, swapTenors, vols, day_count)
    USDLIBOR3M = ql.SwaptionVolatilityMatrix(calendar, business_day_convention, optionTenors, swapTenors, vols, day_count)