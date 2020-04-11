import pytest
import QuantLib as ql
from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from marketdata.interestRateIndices import InterestRateIndex

from test.test_fixtures import *
from utilities.Enums import SwapDirection


def test_USDLIBOR3M_initiation(initialize_test):

    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)

    swap = InterestRateSwap(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.USDLIBOR3M)
    swap.get_price()
    swap.get_fixed_rate()
    swap.get_delta()

def test_EURIBOR6M_initiation(initialize_test):

    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)

    swap = InterestRateSwap(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EURIBOR6M)
    swap.get_price()
    swap.get_fixed_rate()
    swap.get_delta()