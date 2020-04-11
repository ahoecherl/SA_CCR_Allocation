from enum import Enum
import QuantLib as ql
from marketdata import util, interestRateCurves_old
from marketdata.interestRateIndex_old import euribor_3M_index
from marketdata.interestRateIndex_old import InterestRateIndex
from marketdata.interestRateCurves_old import flat_ois_quote
from utilities.FDCalc import fd_simple_quotes

from utilities.Enums import Currency, TradeDirection, TradeType, SwapDirection
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade

fixed_leg_daycount = util.day_count
float_leg_daycount = util.day_count
business_day_convention = util.business_day_convention
end_of_month = False
pricing_engine = ql.DiscountingSwapEngine(interestRateCurves_old.ois_curve_handle)

class InterestRateSwap(InterestRateTrade):

    def __init__(self,
                 notional: float,
                 timeToSwapStart_in_days: float,
                 timeToSwapEnd_in_days: float,
                 swapDirection: SwapDirection,    # Payer is Long, Receiver is Short the underlying
                 currency: Currency = Currency.USD,
                 fixed_rate: float = None,
                 float_spread: float = 0,
                 index= InterestRateIndex.USDLIBOR3M,
                 calendar: ql.Calendar = ql.UnitedStates(),
                 fixed_leg_tenor: ql.Period = ql.Period(3, ql.Months),
                 float_leg_tenor: ql.Period = ql.Period(3, ql.Months),
                 date_generation: ql.DateGeneration = ql.DateGeneration.Forward
                 ):
        """
        :param notional:
        :param timeToSwapStart_in_days:
        :param timeToSwapEnd_in_days:
        :param swapDirection: Payer is Long, Receiver is Short the underlying
        :param currency:
        :param fixed_rate: If not set explicitly the swap will be a par swap
        :param float_spread:
        :param index:
        :param fixed_leg_tenor:
        :param float_leg_tenor:
        """
        self.swapDirection = swapDirection
        if swapDirection == SwapDirection.PAYER:
            tradeDirection = TradeDirection.LONG
            ql_tradeDirection = ql.VanillaSwap.Payer
        if swapDirection == SwapDirection.RECEIVER:
            tradeDirection = TradeDirection.SHORT
            ql_tradeDirection = ql.VanillaSwap.Receiver
        super(InterestRateSwap, self).__init__(
            notional=notional,
            currency=currency,
            s=timeToSwapStart_in_days/360,
            m=timeToSwapEnd_in_days/360,
            e=timeToSwapEnd_in_days/360,
            t=None,
            tradeDirection=tradeDirection,
            tradeType=TradeType.LINEAR
        )
        self.index = index
        settle_date = calendar.advance(util.today, timeToSwapStart_in_days, ql.Days)
        maturity_date = calendar.advance(util.today, timeToSwapEnd_in_days, ql.Days)
        fixed_schedule = ql.Schedule(settle_date, maturity_date, fixed_leg_tenor, calendar, business_day_convention, business_day_convention, date_generation, end_of_month)
        float_schedule = ql.Schedule(settle_date, maturity_date, float_leg_tenor, calendar, business_day_convention, business_day_convention, date_generation, end_of_month)
        if fixed_rate is None:
            dummy_rate = 0.02
            dummy_swap = ql.VanillaSwap(ql_tradeDirection, notional, fixed_schedule, dummy_rate, fixed_leg_daycount, float_schedule, index.value, float_spread, float_leg_daycount)
            dummy_swap.setPricingEngine(pricing_engine)
            fixed_rate = dummy_swap.fairRate()
        self.ql_swap = ql.VanillaSwap(ql_tradeDirection, notional, fixed_schedule, fixed_rate, fixed_leg_daycount, float_schedule, index.value, float_spread, float_leg_daycount)
        self.ql_swap.setPricingEngine(pricing_engine)

    def get_price(self):
        return self.ql_swap.NPV()

    def get_delta(self):
        quote = flat_ois_quote
        delta = fd_simple_quotes([quote], self)
        return delta