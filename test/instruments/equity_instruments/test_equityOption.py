from utilities.Enums import TradeType, TradeDirection, Stock
from instruments.equity_instruments.equityOption import EquityOption
from marketdata.EquityVolatility import EquityVolatility
import pytest
import QuantLib as ql


def test_BSprice():
    option = EquityOption(notional=1, K=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                          underlying=Stock.ADS)
    print(option.get_price())
    assert option.K == 40

def test_equity_simm_delta():
    option2 = EquityOption(notional=1, K=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                          underlying=Stock.ADS)
    simmDelta = option2.get_simm_sensis_equity()
    asdf = 1


def test_equity_simm_vega():
    option2 = EquityOption(notional=1, K=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL,
                           tradeDirection=TradeDirection.LONG,
                           underlying=Stock.ADS)
    simmVega = option2.get_simm_sensis_equityvol()
    asdf = 1