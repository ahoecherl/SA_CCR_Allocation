from Enums import TradeType, TradeDirection, Stock
from instruments.equity_instruments.equityOption import EquityOption
from marketdata.EquityVolatility import EquityVolatilty


def test_BSprice():
    asdf = 1
    asdf = 2
    asdf = 3
    option = EquityOption(notional=1, K=40, m=1, tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                          underlying=Stock.ADS)
    print(option.get_price())
    asdf = 1
