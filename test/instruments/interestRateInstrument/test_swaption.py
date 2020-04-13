from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from marketdata.interestRateIndices import InterestRateIndex
from utilities.Enums import Currency, SwapDirection, TradeDirection
import pytest
from test.test_fixtures import *


def test_USDLIBOR3MSwaption(initialize_test):
    fw_swap = IRS(notional=1000000, timeToSwapStart=ql.Period(1, ql.Years), timeToSwapEnd=ql.Period(20, ql.Years),
                  swapDirection=SwapDirection.PAYER, index=InterestRateIndex.USDLIBOR3M)

    swaption = Swaption(underlyingSwap=fw_swap,
                        optionMaturity_in_days=1 * 360,
                        tradeDirection=TradeDirection.SHORT)
    print(swaption.get_price())
    print(swaption.get_delta())


# @pytest.mark.skip(reason="Pricing of EUR swaptions currently impossible since the pricer can't handle negative rates")
def test_EURIBOR6MSwaption(initialize_test):
    fw_swap = IRS(notional=1000000, timeToSwapStart=ql.Period(1, ql.Years), timeToSwapEnd=ql.Period(20, ql.Years),
                  swapDirection=SwapDirection.PAYER, index=InterestRateIndex.EURIBOR6M)

    swaption = Swaption(underlyingSwap=fw_swap,
                        optionMaturity_in_days=1 * 360,
                        tradeDirection=TradeDirection.SHORT)
    print(swaption.get_price())
    print(swaption.get_delta())


@pytest.mark.skip(reason="TC needs to be rebuilt")
def test_swaption_delta_example(initialize_test, standard_swap, standard_swaption):
    print(standard_swaption.get_price())
    print(standard_swaption.get_delta())
    print(standard_swap.get_price())
    print(standard_swap.get_delta())


@pytest.mark.skip(reason="TC needs to be rebuilt")
def test_swaption_vega(initialize_test, standard_swaption):
    print(standard_swaption.get_vega())
