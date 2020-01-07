from Enums import TradeType, TradeDirection, AssetClass, Stock
from instruments.Trade import Trade


class EquityForward(Trade):

    def __init__(self,
                 notional: float,
                 m: float,
                 S: float,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 underlying: Stock = Stock.ADS):
        """
        Equity Option

        :param notional: Count of underlying shares
        :param S: Underlying Price
        :param m: Time to maturity of the option (in years). Will be used for both, M and T of paragraph 155
        :param tradeType: Can be TradeType.CALL or TradeType.PUT
        :param tradeDirection: Can be TradeDirection.LONG or TradeDirection.SHORT
        """
        self.S = S
        self.underlying = underlying
        super(EquityForward, self).__init__(
            assetClass=AssetClass.EQ,
            tradeType=TradeType.LINEAR,
            tradeDirection=tradeDirection,
            s=0,
            e=m,
            m=m,
            t=m,
            notional=notional
        )