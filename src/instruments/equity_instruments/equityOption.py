import QuantLib as ql

from utilities.Enums import TradeType, TradeDirection, AssetClass, Stock
from instruments.Trade import Trade
from marketdata.EquityVolatility import EquityVolatilty
from marketdata.EquitySpot import EquitySpot
from marketdata.interestRateCurves_old import ois_curve_handle
from marketdata import init_marketdata
from marketdata.util import today
from marketdata.EquityVolatility import Quotes as volatilityQuotes
from marketdata.EquitySpot import Quotes as spotQuotest
from marketdata.interestRateCurves_old import flat_ois_quote
from utilities.FDCalc import fd_simple_quotes


class EquityOption(Trade):

    def __init__(self,
                 notional: float,
                 mat_in_days: float,
                 tradeType: TradeType = TradeType.CALL,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 underlying: Stock = Stock.ADS,
                 K = None):
        """
        Equity Option

        :param notional: Count of underlying shares
        :param mat_in_days: Time to maturity of the option (in days). Will be used for both, M and T of paragraph 155 after being multiplied bei 360
        :param tradeType: Can be TradeType.CALL or TradeType.PUT
        :param tradeDirection: Can be TradeDirection.LONG or TradeDirection.SHORT
        :param K: Strike of option is no strike is given it default to an at the money option
        """
        self.underlying = underlying
        self.K = K if K != None else spotQuotest[self.underlying.name].value()  # no K is given it is the current Spot
        super(EquityOption, self).__init__(
            assetClass=AssetClass.EQ,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            m=mat_in_days*360,
            t=mat_in_days*360,
            notional=notional
        )
        vol_handle = EquityVolatilty.__getattr__(self.underlying.name).value
        spot_handle = EquitySpot.__getattr__(self.underlying.name).value
        self.S = spot_handle.value()
        black_scholes_process = ql.BlackScholesProcess(spot_handle, ois_curve_handle, vol_handle)
        engine = ql.AnalyticEuropeanEngine(black_scholes_process)
        if tradeType.name == TradeType.CALL.name:
            option_type = ql.Option.Call
        else:
            option_type = ql.Option.Put
        payoff = ql.PlainVanillaPayoff(option_type, K)
        maturity_date = today + ql.Period(mat_in_days, ql.Days)
        exercise = ql.EuropeanExercise(maturity_date)
        self.ql_option = ql.VanillaOption(payoff, exercise)
        self.ql_option.setPricingEngine(engine)

    def get_price(self):
        multiplier = self.notional
        if self.tradeDirection == TradeDirection.SHORT:
            multiplier = -1*multiplier
        return multiplier * self.ql_option.NPV()

    def get_delta(self):
        quote = spotQuotes[self.underlying.name]
        delta = fd_simple_quotes([quote], self)
        return delta

    def get_vega(self):
        quote = volatilityQuotes[self.underlying.name]
        vega = fd_simple_quotes([quote], self)
        return vega

    def get_rho(self):
        quote = flat_ois_quote
        rho = fd_simple_quotes([quote], self)
        return rho