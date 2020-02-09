from QuantLib import *

from Enums import TradeType, TradeDirection, AssetClass, Stock
from instruments.Trade import Trade
from pricer.equityOptionPricer import EquityOptionPricer
from marketdata.EquityVolatility import EquityVolatilty
from marketdata.EquitySpot import EquitySpot
from marketdata.InterestRateCurves import ois_curve_handle
from marketdata import init_marketdata
from marketdata.util import today


class EquityOption(Trade):

    def __init__(self,
                 notional: float,
                 K: float,
                 m: float,
                 tradeType: TradeType = TradeType.CALL,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 underlying: Stock = Stock.ADS):
        """
        Equity Option

        :param notional: Count of underlying shares
        :param S: Underlying Price
        :param K: Strike
        :param m: Time to maturity of the option (in years). Will be used for both, M and T of paragraph 155
        :param tradeType: Can be TradeType.CALL or TradeType.PUT
        :param tradeDirection: Can be TradeDirection.LONG or TradeDirection.SHORT
        """
        self.K = K
        self.underlying = underlying
        super(EquityOption, self).__init__(
            assetClass=AssetClass.EQ,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            m=m,
            t=m,
            notional=notional
        )
        vol_handle = EquityVolatilty.__getattr__(self.underlying.name).value
        spot_handle = EquitySpot.__getattr__(self.underlying.name).value
        black_scholes_process = BlackScholesProcess(spot_handle, ois_curve_handle, vol_handle)
        engine = AnalyticEuropeanEngine(black_scholes_process)
        if tradeType == TradeType.CALL:
            option_type = Option.Call
        else:
            option_type = Option.Put
        payoff = PlainVanillaPayoff(option_type, K)
        maturity_date = today + Period(m, Years)
        exercise = EuropeanExercise(maturity_date)
        self.ql_option = VanillaOption(payoff, exercise)
        self.ql_option.setPricingEngine(engine)

    def get_price(self):
        multiplier = self.notional
        if self.tradeDirection == TradeDirection.SHORT:
            multiplier = -1*multiplier
        return multiplier * self.ql_option.NPV()