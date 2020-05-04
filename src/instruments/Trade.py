from typing import Dict, List, Union

from marketdata.fxConverter import fxConvert
from marketdata.interestRateCurves import LiborCurve, OisCurve, InterestRateCurveQuotes
from marketdata.util import today
from margining.Enums import CrifColumn, RiskType
from margining.staticData import periodToLabel1, indexToLabel2
from utilities.Enums import AssetClass, SubClass, TradeType, TradeDirection, Currency
import QuantLib as ql

import utilities.sensiCalc


class Trade():


    def __init__(self,
                 assetClass: AssetClass,
                 notional: float,
                 subClass: SubClass = None,
                 tradeType: TradeType = TradeType.LINEAR,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 m: float = None,
                 s: float = None,
                 e: float = None,
                 t: float = None
                 ):
        """
        Trade object for SA-CCR calculation.

        :param assetClass: Asset Class. Refer to Asset Class Enum
        :param subClass: Sub class of the asset class. Only necessary for certain asset classes e.g. credit.
        :param tradeType: Trade Type. Can be Put, Call or Linear
        :param tradeDirection: Trade Direction. Can be long or short
        :param m: residual maturity in years
        :param s: time until start date of underlying in years (0 if it has already started)
        :param e: time until end date of underlying in years
        :param t: time until final latest contractual
        :param notional: notional of the trade. Denoted in domestic currency for FX trades share or commodity count for EQ and CO asset classes
        """

        self.assetClass = assetClass
        self.subClass = subClass
        self.tradeType = tradeType
        self.tradeDirection = tradeDirection
        self.m = m
        self.s = s
        self.e = e
        self.t = t
        self.notional = notional
        self.simmBaseDict = {CrifColumn.ImModel.value: "SIMM",
                             CrifColumn.PostRegulation.value: "",
                             CrifColumn.CollectRegulation.value: "",
                             CrifColumn.ValuationDate.value: "%4d-%02d-%02d" % (
                             today.year(), today.month(), today.dayOfMonth()),
                             CrifColumn.Notional.value: "",
                             CrifColumn.NotionalCurrency.value: "",
                             CrifColumn.NotionalString.value: "",
                             CrifColumn.Qualifier.value: "",
                             CrifColumn.Bucket.value: "",
                             CrifColumn.Label1.value: "",
                             CrifColumn.Label2.value: ""}
        self.simmBaseDict[CrifColumn.AmountCurrency.value] = self.currency.value
        self.simmBaseDict['tradeId'] = str(id(self))
        self.id = id(self)


    def __str__(self):
        return str({'Instrument': self.__class__.__name__, 'TradeType': self.tradeType.value,
                    'TradeDirection': self.tradeDirection.value, 'Maturity': self.m, 'Startdate': self.s,
                    'Notional': self.notional})


    def get_simm_sensis_ircurve(self, curve: Union[LiborCurve, OisCurve]):
        sensiList = []
        quotes = InterestRateCurveQuotes[curve.name].value
        for period, quote in quotes.items():
            sensiDict = self.simmBaseDict.copy()
            amount = utilities.sensiCalc.dv01_abs_one_bp([quote], self)
            sensiDict[CrifColumn.Amount.value] = '%.10f' % amount
            sensiDict[CrifColumn.RiskType.value] = RiskType.Risk_IRCurve.value
            sensiDict[CrifColumn.Qualifier.value] = self.currency.name
            sensiDict[CrifColumn.Label1.value] = periodToLabel1(period)
            sensiDict[CrifColumn.Label2.value] = indexToLabel2[curve.name]
            sensiDict[CrifColumn.AmountUSD.value] = '%.10f' % fxConvert(self.currency, Currency.USD, amount)
            sensiList.append(sensiDict)
        return sensiList

    def get_simm_sensis(self):
        pass

    def get_price(self):
        pass

    def get_simm_sensis_fx(self) -> List[Dict]:
        sensiList = []
        sensiDict = self.simmBaseDict.copy()
        sensiDict[CrifColumn.RiskType.value] = RiskType.Risk_FX.value
        sensiDict[CrifColumn.Qualifier.value] = self.currency.value

        # these are all single currency interest rate trades. Their fx sensi according to ISDA SIMM is 1 per cent of their NPV.
        amount = self.get_price() * 0.01
        sensiDict[CrifColumn.Amount.value] = '%.10f' % amount
        sensiDict[CrifColumn.AmountUSD.value] = '%.10f' % fxConvert(self.currency, Currency.USD, amount)
        sensiList.append(sensiDict)

        return sensiList

    def get_bumped_copy(self, rel_bump_size):
        pass
