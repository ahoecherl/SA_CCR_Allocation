from typing import List, Dict
import QuantLib as ql

from marketdata.fxConverter import fxConvert
from marketdata.util import today
from simm.Enums import ProductClass, CrifColumn, RiskType
from utilities.Enums import Currency, TradeType, TradeDirection, AssetClass, MaturityBucket
from instruments.Trade import Trade


class InterestRateTrade(Trade):

    def __init__(self,
                 notional: float,
                 currency: Currency,
                 tradeType: TradeType,
                 tradeDirection: TradeDirection,
                 s: float = None,
                 m: float = None,
                 t: float = None,
                 e: float = None):
        self.currency = currency
        super(InterestRateTrade, self).__init__(
            assetClass=AssetClass.IR,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            notional=notional,
            s=s,
            m=m,
            t=t,
            e=e
        )
        self.simmBaseDict[CrifColumn.ProductClass.value] = ProductClass.RatesFX.value
        # all currencies used are Regular volatility currencies and therefore the bucket of IR trades can be hardcoded to 1
        self.simmBaseDict[CrifColumn.Bucket.value] = '1'
        self.simmBaseDict[CrifColumn.AmountCurrency.value] = self.currency.value
        endDate = today + ql.Period(int(e * 360), ql.Days)
        self.simmBaseDict['endDate'] = "%4d-%02d-%02d" % (endDate.year(), endDate.month(), endDate.dayOfMonth())

    def get_maturity_bucket(self):
        if self.m <= 1:
            return MaturityBucket.ONE
        elif 1 < self.m <= 5:
            return MaturityBucket.TWO
        elif 5 < self.m:
            return MaturityBucket.THREE

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
