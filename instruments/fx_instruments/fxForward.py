from Enums import CurrencyPair, TradeDirection, AssetClass, TradeType
from instruments.Trade import Trade
from pricer.fxForwardPricer import FxForwardPricer


class FxForward(Trade):

    def __init__(self,
                 notional: float,
                 currencyPair: CurrencyPair,
                 tradeDirection: TradeDirection,
                 m: float,
                 contractForwardFxRate: float = None,
                 currentForwardFxRate: float = None):
        self.currencyPair = currencyPair
        self.K = contractForwardFxRate
        self.S = currentForwardFxRate
        super(FxForward, self).__init__(
            assetClass = AssetClass.FX,
            tradeType = TradeType.LINEAR,
            tradeDirection = tradeDirection,
            s = 0,
            m = m,
            t = m,
            e = m,
            notional = notional
        )

    def get_pricer(self):
        return FxForwardPricer