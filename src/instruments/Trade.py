from utilities.Enums import AssetClass, SubClass, TradeType, TradeDirection


class Trade:

    ql_instrument = None

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

    def __str__(self):
        return str({'Instrument': self.__class__.__name__, 'TradeType': self.tradeType.value, 'TradeDirection': self.tradeDirection.value, 'Maturity': self.m, 'Startdate': self.s, 'Notional': self.notional})