from marketdata.interestRateCurves_old import InterestRateCurve
from marketdata.interestRateCurves_old import flat_ois_quote
from marketdata.swaptionVolatility import SwaptionVolatility
from utilities.Enums import TradeDirection, TradeType
from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade
import QuantLib as ql
from marketdata.init_marketdata import today
from utilities.FDCalc import fd_simple_quotes


class Swaption(InterestRateTrade):

    def __init__(self,
                 underlyingSwap: InterestRateSwap,
                 optionMaturity_in_days: float,
                 tradeDirection: TradeDirection = TradeDirection.LONG):
        if underlyingSwap.tradeDirection == TradeDirection.LONG:
            tradeType = TradeType.CALL  # A swaption on a payer Swap is a Call Swaption as the call's value raises as the interest rate rises
        else:
            tradeType = TradeType.PUT  # Vice versa the above
        self.K = underlyingSwap.ql_swap.fixedRate()
        super(Swaption, self).__init__(
            notional=underlyingSwap.notional,
            currency=underlyingSwap.currency,
            s=underlyingSwap.s,
            m=underlyingSwap.e,  # assuming the Swaption is physically settled
            t=optionMaturity_in_days / 360,
            e=underlyingSwap.e,
            tradeType=tradeType,
            tradeDirection=tradeDirection
        )
        self.underlying_swap = underlyingSwap
        self.ql_underlying_swap = underlyingSwap.ql_swap
        self.S = self.ql_underlying_swap.fairRate()

        exerciseDate = today + ql.Period(optionMaturity_in_days, ql.Days)
        exercise = ql.EuropeanExercise(exerciseDate)
        swaption = ql.Swaption(self.ql_underlying_swap, exercise)
        swaptionVol = SwaptionVolatility.__getattr__(self.underlying_swap.index.name).value
        real_surface_handle = ql.SwaptionVolatilityStructureHandle(swaptionVol)
        yts = InterestRateCurve.__getattr__(self.underlying_swap.index.name).value
        real_surface_engine = ql.BlackSwaptionEngine(yts, real_surface_handle)
        swaption.setPricingEngine(real_surface_engine)
        self.ql_swaption = swaption

    def get_price(self):
        return self.ql_swaption.NPV()

    def get_delta(self):
        quote = flat_ois_quote
        delta = fd_simple_quotes([quote], self)
        return delta

    def get_vega(self):
        from marketdata.swaptionVolatility import vols
        quotes = [item for sublist in vols for item in sublist]
        vega = fd_simple_quotes(quotes, self)
        return vega