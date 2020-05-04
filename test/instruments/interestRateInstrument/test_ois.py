import pytest
import QuantLib as ql
from pytest import approx

from instruments.interestRateInstrument.ois import OIS
from marketdata.interestRateIndices import InterestRateIndex

from test.test_fixtures import *
from utilities.Enums import SwapDirection


def test_EONIA_initiation(initialize_test):
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)

    swap = OIS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EONIA)
    swap.get_price()
    swap.get_fixed_rate()
    swap.get_delta()


def test_FEDFUNDS_initiation(initialize_test):
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)

    swap = OIS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.FEDFUNDS)
    swap.get_price()
    swap.get_fixed_rate()
    swap.get_delta()

def test_get_bumped_copy():
    bumpsize = 0.01
    option = OIS(notional = 100000,
                 timeToSwapStart=ql.Period(1, ql.Years),
                 timeToSwapEnd=ql.Period(5, ql.Years),
                 swapDirection=SwapDirection.PAYER,
                 index=InterestRateIndex.FEDFUNDS,
                 fixed_rate=0.01)
    option_copy = option.get_bumped_copy(bumpsize)
    assert option_copy.notional == option.notional * (1 + bumpsize)
    assert approx(option_copy.get_price(), abs=0.000001) == option.get_price() * (1 + bumpsize)
    asdf = 1
    for option_sensi, option_copy_sensi in zip(option.get_simm_sensis(), option_copy.get_simm_sensis()):
        assert approx(float(option_sensi['amountUSD']) * (1 + bumpsize), abs=0.000001) == float(
            option_copy_sensi['amountUSD'])