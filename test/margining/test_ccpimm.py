from math import sqrt

import pytest
from pytest import approx

from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
import QuantLib as ql

from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from margining.ccpimm import CCPIMM
from margining.simm import SIMM
from marketdata.EquitySpot import EquitySpot
from marketdata.interestRateIndices import InterestRateIndex
from utilities.Enums import SwapDirection, TradeType, TradeDirection, Stock


def test_equality_with_simm_for_irs():
    irs = IRS(notional=100, timeToSwapStart=ql.Period(2, ql.Days),
              timeToSwapEnd=ql.Period(1, ql.Years),
              swapDirection=SwapDirection.RECEIVER,
              index=InterestRateIndex.EURIBOR6M)

    ois = OIS(notional=100, timeToSwapStart=ql.Period(2, ql.Days),
              timeToSwapEnd=ql.Period(1, ql.Years),
              swapDirection=SwapDirection.RECEIVER,
              index=InterestRateIndex.FEDFUNDS)

    ul_swap = IRS(notional=100, timeToSwapStart=ql.Period(1, ql.Years),
                  timeToSwapEnd=ql.Period(2, ql.Years),
                  swapDirection=SwapDirection.RECEIVER,
                  index=InterestRateIndex.USDLIBOR3M)

    swaption = Swaption(underlyingSwap=ul_swap, optionMaturity=ql.Period(1, ql.Years))

    simm = SIMM()
    simm.add_trades([irs, ois, ul_swap, swaption])

    ccpimm = CCPIMM()
    ccpimm.add_trades([irs, ois, ul_swap, swaption])

    assert simm.get_im_post() != 0
    assert ccpimm.get_im_post() != 0

    assert approx(simm.get_im_post(), rel=0.00001) == ccpimm.get_im_post() * sqrt(10 / 5)


def test_equality_with_simm_for_eq():
    eq_opt = EquityOption(maturity=ql.Period(1, ql.Years),
                          tradeType=TradeType.CALL,
                          tradeDirection=TradeDirection.LONG,
                          underlying=Stock.DBK)

    eq_opt2 = EquityOption(maturity=ql.Period(1, ql.Years),
                           tradeType=TradeType.PUT,
                           tradeDirection=TradeDirection.SHORT,
                           underlying=Stock.ADS,
                           strike=EquitySpot.ADS.value.value() - 5)

    simm = SIMM()
    simm.add_trades([eq_opt, eq_opt2])

    ccpimm = CCPIMM()
    ccpimm.add_trades([eq_opt, eq_opt2])

    assert simm.get_im_post() != 0
    assert ccpimm.get_im_post() != 0

    assert approx(simm.get_im_post(), rel=0.00001) == ccpimm.get_im_post() * sqrt(10 / 3)
