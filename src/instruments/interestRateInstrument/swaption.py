from instruments.interestRateInstrument.interestRateDerivativeConventions import OISConventions, IRSConventions, \
    SwaptionConventions
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from marketdata.fxConverter import fxConvert
from marketdata.interestRateCurves import OisCurve, LiborCurve, InterestRateCurveQuotes, DiscountCurve
from marketdata.swaptionVolatility import SwaptionVolatility, SwaptionVolatilityQuotes
from simm.Enums import CrifColumn, RiskType
from simm.staticData import periodToLabel1
from utilities.Enums import TradeDirection, TradeType, Currency
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade
import QuantLib as ql
from marketdata.init_marketdata import today
from utilities.sensiCalc import fd_simple_quotes, dv01_abs_one_bp
from utilities.timeUtilities import convert_period_to_days


class Swaption(InterestRateTrade):

    def __init__(self,
                 underlyingSwap: InterestRateTrade,
                 optionMaturity: ql.Period,
                 tradeDirection: TradeDirection = TradeDirection.LONG):
        if underlyingSwap.tradeDirection == TradeDirection.LONG:
            tradeType = TradeType.CALL  # A swaption on a payer Swap is a Call Swaption as the call's value raises as the interest rate rises
        else:
            tradeType = TradeType.PUT  # Vice versa the above
        self.K = underlyingSwap.ql_instrument.fixedRate()
        super(Swaption, self).__init__(
            notional=underlyingSwap.notional,
            currency=underlyingSwap.currency,
            s=underlyingSwap.s,
            m=underlyingSwap.e,  # assuming the Swaption is physically settled
            t=convert_period_to_days(optionMaturity),
            e=underlyingSwap.e,
            tradeType=tradeType,
            tradeDirection=tradeDirection
        )
        self.underlying_swap = underlyingSwap
        self.ql_underlying_swap = underlyingSwap.ql_instrument
        self.S = self.ql_underlying_swap.fairRate()

        exerciseDate = today + optionMaturity
        exercise = ql.EuropeanExercise(exerciseDate)
        swaption = ql.Swaption(self.ql_underlying_swap, exercise)
        indexname = self.underlying_swap.index.name
        currency = IRSConventions[indexname].value['Currency']
        self.currency = currency
        discountcuve = DiscountCurve[currency.name].value.value
        swaptionVol = SwaptionVolatility[currency.name].value
        pricer = SwaptionConventions[currency.name].value['Pricer']
        real_surface_engine = pricer(discountcuve, swaptionVol)
        swaption.setPricingEngine(real_surface_engine)
        self.ql_swaption = swaption

    def get_price(self):
        return self.ql_swaption.NPV()

    def get_delta(self):
        quotes = InterestRateCurveQuotes[self.underlying_swap.index.name].value.values()
        delta = fd_simple_quotes(quotes, self)
        return delta

    def get_vega(self):
        from marketdata.swaptionVolatility import vols
        quotes = [item for sublist in vols for item in sublist]
        vega = fd_simple_quotes(quotes, self)
        return vega


    def get_simm_sensis_ircurve(self):
        discCurve = DiscountCurve[self.currency.name].value
        sensiList = []
        forwardCurve = LiborCurve[self.underlying_swap.index.name]
        sensiList += super(Swaption, self).get_simm_sensis_ircurve(forwardCurve)
        sensiList += super(Swaption, self).get_simm_sensis_ircurve(discCurve)
        return sensiList


    def get_simm_sensis_irvol(self):
        sensiList = []
        indexname = self.underlying_swap.index.name
        currency = IRSConventions[indexname].value['Currency']
        swvolquotes = SwaptionVolatilityQuotes[currency.name].value

        for optionTenor in swvolquotes.optionTenors:
            volQuotes = swvolquotes[optionTenor]
            amount = 0
            for volQuote in volQuotes:
                amount += volQuote.value()*fd_simple_quotes([volQuote], self)
            sensiDict = self.simmBaseDict.copy()
            sensiDict[CrifColumn.Amount.value] = '%.10f' % amount
            sensiDict[CrifColumn.RiskType.value] = RiskType.Risk_IRVol.value
            sensiDict[CrifColumn.Qualifier.value] = self.currency.name
            sensiDict[CrifColumn.Label1.value] = periodToLabel1(optionTenor)
            sensiDict[CrifColumn.AmountUSD.value] = '%.10f' % fxConvert(self.currency, Currency.USD, amount)
            sensiList.append(sensiDict)

        return sensiList


    def get_simm_sensis(self):
        return self.get_simm_sensis_fx() + self.get_simm_sensis_ircurve() + self.get_simm_sensis_irvol()
