import pytest
import QuantLib as ql

from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from marketdata.interestRateIndices import InterestRateIndex
from margining.simm import SIMM
from marketdata import init_marketdata
from utilities.Enums import SwapDirection, TradeDirection, TradeType, Stock


@pytest.fixture()
def test_setup_simm():
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)
    swap = IRS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EURIBOR6M, fixed_rate=0.05)
    simm = SIMM()
    simm.add_trades(swap)
    swap2 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.USDLIBOR3M)
    swap3 = IRS(400, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.EURIBOR6M)
    simm.add_trades([swap2, swap3])
    yield simm


def test_remove_single_trade(test_setup_simm):
    simm = test_setup_simm
    ref = simm.trades[1:]
    simm.remove_trades(simm.trades[0])
    assert ref == simm.trades


def test_remove_multiple_trades(test_setup_simm):
    simm = test_setup_simm
    ref = [simm.trades[0]]
    trades = [t for t in simm.trades[1:]]
    simm.remove_trades(trades)
    assert ref == simm.trades


def test_get_im(test_setup_simm):
    simm = test_setup_simm
    assert simm.receive_calculated == False
    assert simm.im_receive is None
    assert simm.upload_id is None
    im1 = simm.get_im_receive()
    upload_id_1 = simm.upload_id
    im1 = simm.get_im_receive()
    assert upload_id_1 == simm.upload_id
    assert simm.receive_calculated == True
    trade = simm.trades[1]
    simm.remove_trades(trade)
    assert simm.receive_calculated == False
    assert simm.im_receive is None
    im2 = simm.get_im_receive()
    assert simm.upload_id > upload_id_1
    assert im1 != im2


@pytest.mark.skip(reason='SIMM sensis for Equity option not implemented yet')
def test_get_im_equity_option():
    pass


def test_get_im_ois():
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(5, ql.Years)
    ois = OIS(1000, tts, tte, swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.FEDFUNDS)
    simm = SIMM()
    simm.add_trades([ois])
    im = simm.get_im_receive()
    ois2 = OIS(1000, tts, tte, swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EONIA)
    simm.add_trades(ois2)
    im = simm.get_im_receive()




def test_get_im_swaption():
    tts = ql.Period(2, ql.Years)
    tte = ql.Period(10, ql.Years)
    swap1 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.USDLIBOR3M)
    swaption1 = Swaption(swap1, ql.Period(2, ql.Years))
    simm = SIMM()
    simm.add_trades(swaption1)
    im = simm.get_im_receive()
    swap2 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.EURIBOR6M)
    simm.add_trades(swap2)
    im = simm.get_im_receive()



def test_get_im_equityoption():
    option2 = EquityOption(notional=100, strike=50, maturity=ql.Period(3, ql.Years), tradeType=TradeType.CALL,
                           tradeDirection=TradeDirection.LONG,
                           underlying=Stock.ADS)
    simm = SIMM()
    simm.add_trades(option2)
    im = simm.get_im_receive()
    asdf = 1


def test_im_post_vs_receive_linear():
    # When setting up an IRS IM post should be = IM receive
    irs = IRS(notional = 100, timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years),
              swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EURIBOR6M)
    simm = SIMM()
    simm.add_trades(irs)
    im_receive = simm.get_im_receive()
    im_post = simm.get_im_post()
    assert im_receive > 0
    assert im_post < 0
    assert -1*im_receive==im_post


def test_im_post_vs_receive_option():
    # When setting up at the money options that expire soon enough the long side of the option should bear significant less IM than the short side
    swap = IRS(notional = 100, timeToSwapStart=ql.Period(6, ql.Months), timeToSwapEnd=ql.Period(1, ql.Years),
              swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EURIBOR6M)
    options = []
    swaption = Swaption(underlyingSwap=swap,optionMaturity=ql.Period(6, ql.Months), tradeDirection=TradeDirection.LONG)
    options.append(swaption)
    eqOpt1 = EquityOption(maturity=ql.Period(2, ql.Months), tradeType=TradeType.CALL, tradeDirection=TradeDirection.LONG)
    options.append(eqOpt1)
    for option in options:
        simm = SIMM()
        simm.add_trades(option)
        im_receive = simm.get_im_receive()
        im_post = -1 * simm.get_im_post()
        assert im_post * 1.1 < im_receive

    eqOpt2 = EquityOption(maturity=ql.Period(2, ql.Months), tradeType=TradeType.PUT,
                          tradeDirection=TradeDirection.SHORT)

    simm = SIMM()
    simm.add_trades(eqOpt2)
    im_receive = simm.get_im_receive()
    im_post = -1 * simm.get_im_post()
    assert im_receive * 1.1 < im_post
