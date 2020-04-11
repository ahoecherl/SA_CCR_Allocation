import pytest
import QuantLib as ql
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
