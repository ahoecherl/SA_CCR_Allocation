from typing import List


class Quote():
    # Marketquote of a financial instrument such as the price of a swap, spot foreign exchange rate, spot stock price
    # etc. The value of a quote is updated when the marketquote is bumped for finite difference calculation or changes
    # through time. This then has a cascading effect on Marketdata objects using the quote and on financial instruments
    # priced with these Marketdata objects.
    pass

class Marketdata():
    # Marketdata objects are e.g. interest rate curves, fx spots, equity volatility surfaces etc.
    # Every marketdata object is constructed based on underlying market quotes. An IRS curve is e.g. bootstrapped
    # from OIS quotes, FRA quotes and Swap quotes. Whenever one of the underlying quotes change the marketdata object
    # is reconstructed. Trade objects can request required marketdata from the marketdata object - e.g. a forward rate
    # for a certain date and a certain tenor from an IRS term structure. Every marketdata object contains a link to the
    # quotes it is based on
    pass

    def __init__(self, quotes: List[Quote]):
        self.quotes = quotes

class InterestRateTermStructure(Marketdata):
    pass

class EquityForwardCurve(Marketdata):
    pass

class EquityVolatilitySurface(Marketdata):
    pass