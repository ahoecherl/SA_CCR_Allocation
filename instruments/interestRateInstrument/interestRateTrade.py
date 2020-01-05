from Enums import Currency, TradeType, TradeDirection, AssetClass
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