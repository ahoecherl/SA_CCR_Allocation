import pytest
from instruments.interestRateInstrument.swaption import Swaption
import QuantLib as ql

from utilities.Enums import TradeDirection


@pytest.fixture(scope='module')
def initialize_test():
    from marketdata import init_marketdata



@pytest.fixture(scope='function')
def standard_swaption(standard_swap):
    swaption = Swaption(underlyingSwap=standard_swap, optionMaturity_in_days=360, tradeDirection=TradeDirection.LONG)
    return swaption
