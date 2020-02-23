from enum import Enum
import QuantLib as ql
from marketdata import util, interestRateCurves
from marketdata.interestRateIndex import euribor_3M_index
from marketdata.interestRateIndex import InterestRateIndex

from utilities.Enums import Currency, TradeDirection, TradeType, SwapDirection
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade

fixed_leg_daycount = util.day_count
float_leg_daycount = util.day_count
swap_calendar = util.calendar
fixed_leg_tenor = ql.Period(6, ql.Months)
float_leg_tenor = ql.Period(3, ql.Months)
business_day_convention = util.business_day_convention
date_generation = ql.DateGeneration.Forward
end_of_month = False
pricing_engine = ql.DiscountingSwapEngine(interestRateCurves.ois_curve_handle)

class InterestRateSwap(InterestRateTrade):

    def __init__(self,
                 notional: float,
                 currency: Currency,
                 timeToSwapStart_in_days: float,
                 timeToSwapEnd_in_days: float,
                 swapDirection: SwapDirection,  # Payer is Long, Receiver is Short the underlying
                 fixed_rate: float = 0.025,
                 float_spread: float = 0.004,
                 index = InterestRateIndex.USDLIBOR3M
                 ):
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
        settle_date = swap_calendar.advance(util.today, int(timeToSwapStart_in_days), ql.Days)
        maturity_date = swap_calendar.advance(util.today, timeToSwapEnd_in_days, ql.Days)
        fixed_schedule = ql.Schedule(settle_date, maturity_date, fixed_leg_tenor, swap_calendar, business_day_convention, business_day_convention, date_generation, end_of_month)
        float_schedule = ql.Schedule(settle_date, maturity_date, float_leg_tenor, swap_calendar, business_day_convention, business_day_convention, date_generation, end_of_month)
        self.ql_swap = ql.VanillaSwap(ql_tradeDirection, notional, fixed_schedule, fixed_rate, fixed_leg_daycount, float_schedule, index.value, float_spread, float_leg_daycount)
        self.ql_swap.setPricingEngine(pricing_engine)

    def get_price(self):
        return self.ql_swap.NPV()