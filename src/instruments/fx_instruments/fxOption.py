from Enums import CurrencyPair, TradeDirection, AssetClass, TradeType
from instruments.Trade import Trade
from pricer.fxOptionPricer import FxOptionPricer


class FxOption(Trade):

    def __init__(self,
                 notional: float,
                 currencyPair: CurrencyPair,
                 m: float,
                 strike: float,
                 currentForwardFxRate: float,
                 tradeType: TradeType = TradeType.CALL,
                 tradeDirection: TradeDirection = TradeDirection.LONG
                 ):
        self.currencyPair = currencyPair
        self.K = strike
        self.S = currentForwardFxRate
        super(FxOption, self).__init__(
            assetClass = AssetClass.FX,
            tradeType = tradeType,
            tradeDirection = tradeDirection,
            s = 0,
            m = m,
            t = m,
            e = m,
            notional = notional
        )

    def get_pricer(self):
        return FxOptionPricer