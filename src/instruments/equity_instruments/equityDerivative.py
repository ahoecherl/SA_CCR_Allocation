from typing import Dict, List
import QuantLib as ql

from instruments.Trade import Trade
from marketdata.EquitySpot import EquitySpotQuote
from marketdata.fxConverter import fxConvert
from marketdata.util import today
from simm.Enums import CrifColumn, RiskType, EquityStaticData, ProductClass
from utilities.Enums import Currency
from utilities.sensiCalc import dv01_rel_one_percent


class EquityDerivative(Trade):

    def __init__(self,
                 assetClass,
                 tradeType,
                 tradeDirection,
                 m,
                 t,
                 notional):
        super(EquityDerivative, self).__init__(
            assetClass=assetClass,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            m=m,
            t=t,
            notional=notional
        )
        self.simmBaseDict[CrifColumn.ProductClass.value] = ProductClass.Equity.value
        endDate = today + ql.Period(int(m), ql.Days)
        self.simmBaseDict['endDate'] = "%4d-%02d-%02d" % (endDate.year(), endDate.month(), endDate.dayOfMonth())


    def get_simm_sensis_equity(self) -> List[Dict]:
        sensiList = []
        sensiDict = self.simmBaseDict.copy()
        sensiDict[CrifColumn.RiskType.value] = RiskType.Risk_Equity.value
        sensiDict[CrifColumn.Qualifier.value] = EquityStaticData[self.underlying.name].value[CrifColumn.Qualifier]
        sensiDict[CrifColumn.Bucket.value] = EquityStaticData[self.underlying.name].value[CrifColumn.Bucket]
        quote = EquitySpotQuote[self.underlying.name].value
        amount = dv01_rel_one_percent([quote], self)
        sensiDict[CrifColumn.Amount.value] = '%.10f' % amount
        sensiDict[CrifColumn.AmountUSD.value] = '%.10f' % fxConvert(self.currency, Currency.USD, amount)
        sensiList.append(sensiDict)
        return sensiList

