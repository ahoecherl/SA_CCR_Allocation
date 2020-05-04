from pytest import approx

from utilities.Enums import TradeType, TradeDirection, Stock
from instruments.equity_instruments.equityOption import EquityOption
from marketdata.EquityVolatility import EquityVolatility
import pytest
import QuantLib as ql


def test_BSprice():
    option = EquityOption(notional=1, strike=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                          underlying=Stock.ADS)
    print(option.get_price())
    assert option.K == 40

def test_equity_simm_delta():
    option2 = EquityOption(notional=1, strike=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                           underlying=Stock.ADS)
    simmDelta = option2.get_simm_sensis_equity()
    asdf = 1


def test_equity_simm_vega():
    option2 = EquityOption(notional=1, strike=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL,
                           tradeDirection=TradeDirection.LONG,
                           underlying=Stock.ADS)
    simmVega = option2.get_simm_sensis_equityvol()
    asdf = 1


def test_get_bumped_copy():
    bumpsize = 0.01
    option = EquityOption(notional=100, strike=40, maturity=ql.Period(1, ql.Years), tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG,
                          underlying=Stock.ADS)
    option_copy = option.get_bumped_copy(bumpsize)
    assert option_copy.notional == option.notional*(1+bumpsize)
    assert option_copy.get_price() == option.get_price()*(1+bumpsize)
    asdf =1
    for option_sensi, option_copy_sensi in zip(option.get_simm_sensis(), option_copy.get_simm_sensis()):
        assert approx(float(option_sensi['amountUSD'])*(1+bumpsize), abs=0.000001) == float(option_copy_sensi['amountUSD'])