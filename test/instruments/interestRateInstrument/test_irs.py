import pytest
import QuantLib as ql
from instruments.interestRateInstrument.irs import IRS
from marketdata.interestRateIndices import InterestRateIndex

from test.test_fixtures import *
from utilities.Enums import SwapDirection


def test_USDLIBOR3M_initiation(initialize_test):
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)

    swap = IRS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.USDLIBOR3M)
    swap.get_price()
    swap.get_fixed_rate()
    swap.get_delta()


def test_EURIBOR6M_initiation(initialize_test):
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)

    swap = IRS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EURIBOR6M)
    swap.get_price()
    swap.get_fixed_rate()
    swap.get_delta()


def test_simm_sensi_ircurve():
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)
    swap = IRS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EURIBOR6M)
    ircurve_sensis = swap.get_simm_sensis_ircurve()
    asdf = 1


def test_simm_sensi():
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)
    swap = IRS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EURIBOR6M, fixed_rate=0.05)
    fx_sensis = swap.get_simm_sensis_fx()
    asdf = 1


def test_simm_sensi():
    tts = ql.Period(2, ql.Days)
    tte = ql.Period(10, ql.Years)
    swap = IRS(100, tts, tte, SwapDirection.PAYER, InterestRateIndex.EURIBOR6M, fixed_rate=0.05)
    sensis = swap.get_simm_sensis()
    asdf = 1
