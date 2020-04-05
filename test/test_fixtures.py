import pytest
from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from instruments.interestRateInstrument.swaption import Swaption
from marketdata.interestRateIndex import InterestRateIndex
from marketdata.util import business_day_convention, day_count, today
import QuantLib as ql

from utilities.Enums import SwapDirection, Currency, TradeDirection


@pytest.fixture(scope='module')
def initialize_test():
    from marketdata import init_marketdata


@pytest.fixture(scope='function')
def standard_swap():
    calendar = ql.TARGET()
    swap = InterestRateSwap(notional=1000000, timeToSwapStart_in_days=360, timeToSwapEnd_in_days=720,
                            swapDirection=SwapDirection.RECEIVER, currency=Currency.EUR,
                            index=InterestRateIndex.EURIBOR3M, calendar=calendar)
    return swap


@pytest.fixture(scope='function')
def standard_swaption(standard_swap):
    swaption = Swaption(underlyingSwap=standard_swap, optionMaturity_in_days=360, tradeDirection=TradeDirection.LONG)
    return swaption
