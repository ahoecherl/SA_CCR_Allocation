import pytest
import QuantLib as ql

from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from marketdata.interestRateIndices import InterestRateIndex
from simm.simm import SIMM
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
    id = simm.trades[0].id
    simm.remove_trades(id)
    assert ref == simm.trades


def test_remove_multiple_trades(test_setup_simm):
    simm = test_setup_simm
    ref = [simm.trades[0]]
    ids = [t.id for t in simm.trades[1:]]
    simm.remove_trades(ids)
    assert ref == simm.trades


def test_get_im(test_setup_simm):
    simm = test_setup_simm
    assert simm.calculated == False
    assert simm.im is None
    assert simm.upload_id is None
    im1 = simm.get_im()
    upload_id_1 = simm.upload_id
    im1 = simm.get_im()
    assert upload_id_1 == simm.upload_id
    assert simm.calculated == True
    trade_id = simm.trades[1].id
    simm.remove_trades(trade_id)
    assert simm.calculated == False
    assert simm.im is None
    im2 = simm.get_im()
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
    im = simm.get_im()
    ois2 = OIS(1000, tts, tte, swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EONIA)
    simm.add_trades(ois2)
    im = simm.get_im()




def test_get_im_swaption():
    tts = ql.Period(2, ql.Years)
    tte = ql.Period(10, ql.Years)
    swap1 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.USDLIBOR3M)
    swaption1 = Swaption(swap1, ql.Period(2, ql.Years))
    simm = SIMM()
    simm.add_trades(swaption1)
    im = simm.get_im()
    swap2 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.EURIBOR6M)
    simm.add_trades(swap2)
    im = simm.get_im()



def test_get_im_equityoption():
    option2 = EquityOption(notional=100, K=50, maturity=ql.Period(3, ql.Years), tradeType=TradeType.CALL,
                           tradeDirection=TradeDirection.LONG,
                           underlying=Stock.ADS)
    simm = SIMM()
    simm.add_trades(option2)
    im = simm.get_im()
    asdf = 1
