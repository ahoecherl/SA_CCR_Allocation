import pytest
from instruments.interestRateInstrument.swaption import Swaption
import QuantLib as ql

from utilities.Enums import TradeDirection


@pytest.fixture(scope='module')
def initialize_test():
    from marketdata import init_marketdata



@pytest.fixture(scope='function')
def standard_swaption(standard_swap):
    swaption = Swaption(underlyingSwap=standard_swap, optionMaturity=360, tradeDirection=TradeDirection.LONG)
    return swaption


@pytest.fixture(scope='function')
def init_ca():
    from instruments.interestRateInstrument.ois import OIS
    from instruments.interestRateInstrument.irs import IRS
    from instruments.equity_instruments.equityOption import EquityOption
    from collateralAgreement.collateralAgreement import CollateralAgreement
    from sa_ccr.sa_ccr import SA_CCR
    trade1 = OIS(fixed_rate=0.01)
    trade2 = IRS(fixed_rate=0.01)
    trade3 = Swaption()
    trade4 = EquityOption()
    # trade4 = EquityOption()
    ca = CollateralAgreement()
    ca.link_sa_ccr_instance(SA_CCR(ca))
    ca.add_trades([trade1, trade2, trade3, trade4])
    yield ca
