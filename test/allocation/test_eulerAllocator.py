import pytest
import QuantLib as ql

from allocation.eulerAllocator import EulerAllocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from marketdata import init_marketdata
from sa_ccr.sa_ccr import SA_CCR


def test_for_smoke():
    trade1 = OIS(fixed_rate=0.01)
    trade2 = IRS(fixed_rate=0.01)
    trade3 = Swaption()
    trade4 = EquityOption()
    ca = CollateralAgreement()
    ca.link_sa_ccr_instance(SA_CCR(ca))
    ca.add_trades([trade1, trade2, trade3, trade4])
    eulerAllocator = EulerAllocator(ca)
    allocated_vm = eulerAllocator.allocate_vm()
    allocated_im = eulerAllocator.allocate_im()
    allocated_ead = eulerAllocator.allocate_ead()
    ca.sync_im_model = False
    ca.sync_vm_model = False
    allocated_ead2 = eulerAllocator.allocate_ead()
    

    asdf = 1