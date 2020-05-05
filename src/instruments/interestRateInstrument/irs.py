from typing import Dict, List

import QuantLib as ql
from pytest import approx

from marketdata.fxConverter import fxConvert
from marketdata.interestRateCurves import InterestRateCurveQuotes, LiborCurve, DiscountCurve
from marketdata.interestRateIndices import InterestRateIndex
from margining.Enums import CrifColumn, RiskType
from margining.staticData import periodToLabel1, indexToLabel2
from utilities.Enums import SwapDirection, TradeDirection, TradeType, Currency
from utilities.sensiCalc import fd_simple_quotes, dv01_abs_one_bp
from utilities.timeUtilities import convert_period_to_days
from instruments.interestRateInstrument.interestRateDerivativeConventions import IRSConventions
from marketdata.util import today
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade


class IRS(InterestRateTrade):

    def __init__(self,
                 notional = 100,
                 timeToSwapStart: ql.Period = ql.Period(1, ql.Years),
                 timeToSwapEnd: ql.Period = ql.Period(2, ql.Years),
                 swapDirection: SwapDirection = SwapDirection.PAYER,
                 index: InterestRateIndex = InterestRateIndex.EURIBOR6M,
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

        currency = IRSConventions[index.name].value['Currency']
        calendar = IRSConventions[index.name].value['Calendar']
        dateRoll = IRSConventions[index.name].value['DateRoll']
        dateGeneration = IRSConventions[index.name].value['DateGeneration']
        endOfMonth = IRSConventions[index.name].value['EndOfMonth']
        fixedLegTenor = ql.Period(IRSConventions[index.name].value['FixedFrequency'])
        floatLegTenor = ql.Period(IRSConventions[index.name].value['FloatFrequency'])
        floatDayCount = IRSConventions[index.name].value['FloatDayCount']
        fixedDayCount = IRSConventions[index.name].value['FixedDayCount']

        self.swapDirection = swapDirection
        if swapDirection == SwapDirection.PAYER:
            tradeDirection = TradeDirection.LONG
            ql_tradeDirection = ql.VanillaSwap.Payer
        if swapDirection == SwapDirection.RECEIVER:
            tradeDirection = TradeDirection.SHORT
            ql_tradeDirection = ql.VanillaSwap.Receiver
        self.ql_timeToSwapStart = timeToSwapStart
        self.ql_timeToSwapEnd = timeToSwapEnd
        super(IRS, self).__init__(
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
        self.float_spread = float_spread

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
        # performs a simultaneous absolute parallel shift of all quotes of the LIBOR curve
        quotes = InterestRateCurveQuotes[self.index.name].value.values()
        delta = fd_simple_quotes(quotes, self)
        return delta

    def get_simm_sensis_ircurve(self) -> List[Dict]:
        discCurve = DiscountCurve[self.currency.name].value
        sensiList = []
        forwardCurve = LiborCurve[self.index.name]
        sensiList += super(IRS, self).get_simm_sensis_ircurve(forwardCurve)
        sensiList += super(IRS, self).get_simm_sensis_ircurve(discCurve)
        return sensiList

    def get_simm_sensis(self):
        if self.lazy_simm_sensi_calculation and self.simm_sensis is not None:
            return self.simm_sensis
        self.simm_sensis = self.get_simm_sensis_fx() + self.get_simm_sensis_ircurve()
        return self.simm_sensis

    def get_bumped_copy(self, rel_bump_size: float = 0.00001):
        new_notional = self.notional*(1+rel_bump_size)
        return IRS(notional = new_notional,
                   timeToSwapStart=self.ql_timeToSwapStart,
                   timeToSwapEnd=self.ql_timeToSwapEnd,
                   swapDirection=self.swapDirection,
                   index=self.index,
                   fixed_rate=self.get_fixed_rate(),
                   float_spread=self.float_spread)
