import QuantLib as ql
from marketdata.interestRateCurves import InterestRateCurveQuotes, OisCurve
from marketdata.interestRateIndices import InterestRateIndex
from utilities.Enums import SwapDirection, TradeDirection, TradeType
from utilities.FDCalc import fd_simple_quotes
from utilities.timeUtilities import convert_period_to_days
from instruments.interestRateInstrument.interestRateDerivativeConventions import OISConventions
from marketdata.util import today
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade


class OIS(InterestRateTrade):
    def __init__(self,
                 notional,
                 timeToSwapStart: ql.Period,
                 timeToSwapEnd: ql.Period,
                 swapDirection: SwapDirection,
                 index: InterestRateIndex,
                 fixed_rate: float = None,
                 float_spread: float = 0
                 ):
        """

        :param notional:
        :param timeToSwapStart:
        :param timeToSwapEnd:
        :param swapDirection:
        :param index:
        :param fixed_rate:
        :param float_spread:
        """

        currency = OISConventions[index.name].value['Currency']
        calendar = OISConventions[index.name].value['Calendar']
        dateRoll = OISConventions[index.name].value['DateRoll']
        endOfMonth = OISConventions[index.name].value['EndOfMonth']
        fixedPeriod = ql.Period(OISConventions[index.name].value['FixedFrequency'])
        dateGeneration = OISConventions[index.name].value['DateGeneration']
        dayCount = OISConventions[index.name].value['DayCount']

        self.swapDirection = swapDirection,
        if swapDirection == SwapDirection.PAYER:
            tradeDirection = TradeDirection.LONG
            ql_tradeDirection = ql.OvernightIndexedSwap.Payer
        if swapDirection == SwapDirection.RECEIVER:
            tradeDirection = TradeDirection.SHORT
            ql_tradeDirection = ql.OvernightIndexedSwap.Receiver
        super(OIS, self).__init__(
            notional=notional,
            currency=currency,
            s=convert_period_to_days(timeToSwapStart) / 360,
            m=convert_period_to_days(timeToSwapEnd) / 360,
            e=convert_period_to_days(timeToSwapEnd) / 360,
            t=None,
            tradeDirection=tradeDirection,
            tradeType=TradeType.LINEAR
        )
        self.index = index
        settle_date = calendar.advance(today, timeToSwapStart, dateRoll, endOfMonth)
        maturity_date = calendar.advance(today, timeToSwapEnd, dateRoll, endOfMonth)
        schedule = ql.Schedule(settle_date, maturity_date, fixedPeriod, calendar, dateRoll, dateRoll, dateGeneration,
                               endOfMonth)

        pricing_engine = ql.DiscountingSwapEngine(OisCurve[index.name].value)

        if fixed_rate is None:
            dummy_rate = 0.02
            dummy_ois = ql.OvernightIndexedSwap(ql_tradeDirection, notional, schedule, dummy_rate, dayCount, index.value)
            dummy_ois.setPricingEngine(pricing_engine)
            fixed_rate = dummy_ois.fairRate()

        self.ql_instrument = ql.OvernightIndexedSwap(ql_tradeDirection, notional, schedule, fixed_rate, dayCount, index.value)
        self.ql_instrument.setPricingEngine(pricing_engine)

    def get_price(self):
        return self.ql_instrument.NPV()

    def get_par_rate(self):
        return self.ql_instrument.fairRate()

    def get_fixed_rate(self):
        return self.ql_instrument.fixedRate()

    def get_delta(self):
        # performs a simultaneous absolute parallel shift of all quotes used for building the OIS curve
        quotes = InterestRateCurveQuotes[self.index.name].value.values()
        delta = fd_simple_quotes(quotes, self)
        return delta
