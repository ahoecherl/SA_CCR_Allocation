from utilities.Enums import TradeType, TradeDirection, Stock
from instruments.equity_instruments.equityOption import EquityOption
from marketdata.EquityVolatility import EquityVolatilty


def test_BSprice():
    option = EquityOption(notional=1, K=40, mat_in_days=1, tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                          underlying=Stock.ADS)
    print(option.get_price())
