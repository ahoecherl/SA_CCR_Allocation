import QuantLib as ql

from instruments.equity_instruments.equityDerivative import EquityDerivative
from marketdata.interestRateCurves import OisCurve, InterestRateCurveQuotes, DiscountCurve
from utilities.Enums import TradeType, TradeDirection, AssetClass, Stock
from marketdata.EquityVolatility import EquityVolatilty
from marketdata.EquitySpot import EquitySpot
from marketdata.util import today
from marketdata.EquityVolatility import Quotes as volatilityQuotes
from marketdata.EquitySpot import EquitySpotQuote
from utilities.sensiCalc import fd_simple_quotes
from utilities.timeUtilities import convert_period_to_days

discounting_curve = OisCurve.EONIA

class EquityOption(EquityDerivative):

    def __init__(self,
                 notional: float,
                 maturity: ql.Period(),
                 tradeType: TradeType = TradeType.CALL,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 underlying: Stock = Stock.ADS,
                 K = None):
        """
        Equity Option

        :param notional: Count of underlying shares
        :param maturity: Time to maturity of the option (in days). Will be used for both, M and T of paragraph 155 after being multiplied bei 360
        :param tradeType: Can be TradeType.CALL or TradeType.PUT
        :param tradeDirection: Can be TradeDirection.LONG or TradeDirection.SHORT
        :param K: Strike of option is no strike is given it default to an at the money option
        """
        self.underlying = underlying
        self.K = K if K != None else EquitySpotQuote[self.underlying.name].value.value()  # no K is given it is the current Spot
        self.currency = underlying.value['Currency']
        super(EquityOption, self).__init__(
            assetClass=AssetClass.EQ,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            m=convert_period_to_days(maturity),
            t=convert_period_to_days(maturity),
            notional=notional
        )
        vol_handle = EquityVolatilty.__getattr__(self.underlying.name).value
        spot_handle = EquitySpot.__getattr__(self.underlying.name).value
        self.S = spot_handle.value()
        black_scholes_process = ql.BlackScholesProcess(spot_handle, discounting_curve.value, vol_handle)
        engine = ql.AnalyticEuropeanEngine(black_scholes_process)
        if tradeType.name == TradeType.CALL.name:
            option_type = ql.Option.Call
        else:
            option_type = ql.Option.Put
        payoff = ql.PlainVanillaPayoff(option_type, K)
        maturity_date = today + maturity
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
        quotes = InterestRateCurveQuotes[discounting_curve.name].value.values()
        rho = fd_simple_quotes(quotes, self)
        return rho

    def get_simm_sensis_ircurve(self):
        sensis = []
        curve = DiscountCurve[self.currency].value
        sensis += super(EquityOption, self).get_simm_sensis_ircurve(curve)
        return sensis

    def get_simm_sensis_equityvol(self):
        pass


    def get_simm_sensis(self):
        return self.get_simm_sensis_fx \
               + self.get_simm_sensis_ircurve() \
               + self.get_simm_sensis_equity() \
               + self.get_simm_sensis_equityvol
