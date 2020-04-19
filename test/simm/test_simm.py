import pytest
import QuantLib as ql

from instruments.interestRateInstrument.irs import IRS
from marketdata.interestRateIndices import InterestRateIndex
from simm.simm import SIMM
from marketdata import init_marketdata
from utilities.Enums import SwapDirection

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