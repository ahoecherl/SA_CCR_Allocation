import QuantLib as ql
from marketdata.interestRateCurves import InterestRateCurveQuotes, LiborCurve
from marketdata.interestRateIndices import InterestRateIndex
from utilities.Enums import SwapDirection, TradeDirection, TradeType
from utilities.FDCalc import fd_simple_quotes
from utilities.timeUtilities import convert_period_to_days
from instruments.interestRateInstrument.interestRateDerivativeConventions import InterestRateSwapConventions
from marketdata.util import today
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade


class InterestRateSwap(InterestRateTrade):

    def __init__(self,
                 notional,
                 timeToSwapStart: ql.Period,
                 timeToSwapEnd: ql.Period,
                 swapDirection: SwapDirection,
                 index: InterestRateIndex,
                 fixed_rate: float = None,
                 float_spread: float = 0,
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

        currency = InterestRateSwapConventions[index.name].value['Currency']
        calendar = InterestRateSwapConventions[index.name].value['Calendar']
        dateRoll = InterestRateSwapConventions[index.name].value['DateRoll']
        dateGeneration = InterestRateSwapConventions[index.name].value['DateGeneration']
        endOfMonth = InterestRateSwapConventions[index.name].value['EndOfMonth']
        fixedLegTenor = ql.Period(InterestRateSwapConventions[index.name].value['FixedFrequency'])
        floatLegTenor = ql.Period(InterestRateSwapConventions[index.name].value['FloatFrequency'])
        floatDayCount = InterestRateSwapConventions[index.name].value['FloatDayCount']
        fixedDayCount = InterestRateSwapConventions[index.name].value['FixedDayCount']

        self.swapDirection = swapDirection,
        if swapDirection == SwapDirection.PAYER:
            tradeDirection = TradeDirection.LONG
            ql_tradeDirection = ql.VanillaSwap.Payer
        if swapDirection == SwapDirection.RECEIVER:
            tradeDirection = TradeDirection.SHORT
            ql_tradeDirection = ql.VanillaSwap.Receiver
        super(InterestRateSwap, self).__init__(
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
        fixed_schedule = ql.Schedule(settle_date, maturity_date, fixedLegTenor, calendar, dateRoll, dateRoll,
                                     dateGeneration, endOfMonth)
        float_schedule = ql.Schedule(settle_date, maturity_date, floatLegTenor, calendar, dateRoll, dateRoll,
                                     dateGeneration, endOfMonth)

        pricing_engine = ql.DiscountingSwapEngine(LiborCurve[index.name].value)

        if fixed_rate is None:
            dummy_rate = 0.02
            dummy_swap = ql.VanillaSwap(ql_tradeDirection, notional, fixed_schedule, dummy_rate, fixedDayCount,
                                        float_schedule, index.value, float_spread, floatDayCount)
            dummy_swap.setPricingEngine(pricing_engine)
            fixed_rate = dummy_swap.fairRate()

        self.ql_instrument = ql.VanillaSwap(ql_tradeDirection, notional, fixed_schedule, fixed_rate, fixedDayCount,
                                            float_schedule, index.value, float_spread, floatDayCount)
        self.ql_instrument.setPricingEngine(pricing_engine)

    def get_price(self):
        return self.ql_instrument.NPV()

    def get_par_rate(self):
        return self.ql_instrument.fairRate()

    def get_fixed_rate(self):
        return self.ql_instrument.fixedRate()

    def get_delta(self):
        # performs a simultaneous absolute parallel shift of all quotes
        quotes = InterestRateCurveQuotes[self.index.name].value.values()
        delta = fd_simple_quotes(quotes, self)
        return delta
