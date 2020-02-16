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

    def get_maturity_bucket(self):
        if self.m <= 1:
            return MaturityBucket.ONE
        elif 1 < self.m <= 5:
            return MaturityBucket.TWO
        elif 5 < self.m:
            return MaturityBucket.THREE
