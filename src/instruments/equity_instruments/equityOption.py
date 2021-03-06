import QuantLib as ql

from allocation.Enums import FdApproach
from instruments.equity_instruments.equityDerivative import EquityDerivative
from marketdata.fxConverter import fxConvert
from marketdata.interestRateCurves import OisCurve, InterestRateCurveQuotes, DiscountCurve
from margining.Enums import CrifColumn, EquityStaticData, RiskType
from margining.staticData import periodToLabel1
from utilities.Enums import TradeType, TradeDirection, AssetClass, Stock, Currency
from marketdata.EquityVolatility import EquityVolatility, EquityVolatilityQuotes
from marketdata.EquitySpot import EquitySpot
from marketdata.util import today
from marketdata.EquitySpot import EquitySpotQuote
from utilities.timeUtilities import convert_period_to_days


class EquityOption(EquityDerivative):

    def __init__(self,
                 maturity: ql.Period() = ql.Period(1, ql.Years),
                 tradeType: TradeType = TradeType.CALL,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 underlying: Stock = Stock.ADS,
                 notional: float = 1,
                 strike: float = None):
        """
        Equity Option

        :param notional: Count of underlying shares
        :param maturity: Time to maturity of the option (in days). Will be used for both, M and T of paragraph 155 after being divided by 360
        :param tradeType: Can be TradeType.CALL or TradeType.PUT
        :param tradeDirection: Can be TradeDirection.LONG or TradeDirection.SHORT
        :param strike: Strike of option is no strike is given it default to an at the money option
        """
        self.underlying = underlying
        self.K = strike if strike != None else EquitySpotQuote[
            self.underlying.name].value.value()  # no K is given it is the current Spot
        self.currency = underlying.value['Currency']
        self.ql_maturity = maturity
        super(EquityOption, self).__init__(
            assetClass=AssetClass.EQ,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            m=convert_period_to_days(maturity) / 360,
            t=convert_period_to_days(maturity) / 360,
            notional=notional
        )
        vol_handle = EquityVolatility[self.underlying.name].value
        spot_handle = EquitySpot[self.underlying.name].value
        self.S = spot_handle.value()
        discounting_curve = DiscountCurve[self.currency.name].value
        black_scholes_process = ql.BlackScholesProcess(spot_handle, discounting_curve.value, vol_handle)
        engine = ql.AnalyticEuropeanEngine(black_scholes_process)
        if tradeType.name == TradeType.CALL.name:
            option_type = ql.Option.Call
        else:
            option_type = ql.Option.Put
        payoff = ql.PlainVanillaPayoff(option_type, self.K)
        maturity_date = today + maturity
        exercise = ql.EuropeanExercise(maturity_date)
        self.ql_option = ql.VanillaOption(payoff, exercise)
        self.ql_option.setPricingEngine(engine)

    def get_price(self):
        multiplier = self.notional
        if self.tradeDirection == TradeDirection.SHORT:
            multiplier = -1 * multiplier
        return multiplier * self.ql_option.NPV()

    def get_simm_sensis_ircurve(self):
        sensis = []
        curve = DiscountCurve[self.currency.name].value
        sensis += super(EquityOption, self).get_simm_sensis_ircurve(curve)
        return sensis

    def get_simm_sensis_equityvol(self):
        sensis = []
        volHandle = EquityVolatility[self.underlying.name].value
        volQuotes = EquityVolatilityQuotes[self.underlying.name].value
        p0 = self.get_price()

        simmBase2 = self.simmBaseDict.copy()
        simmBase2[CrifColumn.Qualifier.value] = EquityStaticData[self.underlying.name].value[CrifColumn.Qualifier]
        simmBase2[CrifColumn.Bucket.value] = EquityStaticData[self.underlying.name].value[CrifColumn.Bucket]
        simmBase2[CrifColumn.RiskType.value] = RiskType.Risk_EquityVol.value
        for optionMaturity in volQuotes.optionMaturities:
            sensiDict = simmBase2.copy()
            volHandle.linkTo(volQuotes.get_atm_shifted_surface_abs_one_pct(optionMaturity))
            amount = self.get_price() - p0
            sensiDict[CrifColumn.Label1.value] = periodToLabel1(optionMaturity)
            sensiDict[CrifColumn.Amount.value] = '%.10f' % amount
            sensiDict[CrifColumn.AmountUSD.value] = '%.10f' % fxConvert(self.currency, Currency.USD, amount)
            sensis.append(sensiDict)

        volHandle.linkTo(volQuotes.ql_BlackVarianceSurface)
        return sensis

    def get_simm_sensis(self):
        if self.lazy_simm_sensi_calculation and self.simm_sensis is not None:
            return self.simm_sensis
        self.simm_sensis = self.get_simm_sensis_fx() \
                           + self.get_simm_sensis_ircurve() \
                           + self.get_simm_sensis_equity() \
                           + self.get_simm_sensis_equityvol()
        return self.simm_sensis

    def get_bumped_copy(self, rel_bump_size: float = 0.00001, abs_bump_size: float = 0.01, bump_approach: FdApproach = FdApproach.Relative):
        if bump_approach == FdApproach.Relative:
            new_notional = self.notional * (1 + rel_bump_size)
        elif bump_approach == FdApproach.Absolute:
            new_notional = self.notional+abs_bump_size
        else:
            raise (Exception('Weird stuff is happening'))

        return EquityOption(maturity=self.ql_maturity,
                            tradeType=self.tradeType,
                            tradeDirection=self.tradeDirection,
                            underlying=self.underlying,
                            notional=new_notional,
                            strike=self.K
                            )
