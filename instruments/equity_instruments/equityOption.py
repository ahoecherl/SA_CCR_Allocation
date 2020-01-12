from Enums import TradeType, TradeDirection, AssetClass, Stock
from instruments.Trade import Trade
from pricer.equityOptionPricer import EquityOptionPricer


class EquityOption(Trade):

    def __init__(self,
                 notional: float,
                 S: float,
                 K: float,
                 m: float,
                 tradeType: TradeType = TradeType.CALL,
                 tradeDirection: TradeDirection = TradeDirection.LONG,
                 underlying: Stock = Stock.ADS):
        """
        Equity Option

        :param notional: Count of underlying shares
        :param S: Underlying Price
        :param K: Strike
        :param m: Time to maturity of the option (in years). Will be used for both, M and T of paragraph 155
        :param tradeType: Can be TradeType.CALL or TradeType.PUT
        :param tradeDirection: Can be TradeDirection.LONG or TradeDirection.SHORT
        """
        self.S = S
        self.K = K
        self.underlying = underlying
        super(EquityOption, self).__init__(
            assetClass=AssetClass.EQ,
            tradeType=tradeType,
            tradeDirection=tradeDirection,
            m=m,
            t=m,
            notional=notional
        )

    def get_pricer(self):
        return EquityOptionPricer