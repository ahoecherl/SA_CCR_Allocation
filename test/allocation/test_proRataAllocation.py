import pytest

from allocation.eulerAllocator import EulerAllocator
from allocation.proRataAllocator import ProRataAllocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from sa_ccr.sa_ccr import SA_CCR


def test_for_smoke():
    trade1 = OIS(fixed_rate=0.01)
    trade2 = IRS(fixed_rate=0.01)
    trade3 = Swaption()
    trade4 = EquityOption()
    ca = CollateralAgreement()
    ca.link_sa_ccr_instance(SA_CCR(ca))
    ca.add_trades([trade1, trade2, trade3, trade4])
    proRataAllocator = ProRataAllocator(ca)
    allocated_vm = proRataAllocator.allocate_vm()
    allocated_im = proRataAllocator.allocate_im()
    allocated_ead = proRataAllocator.allocate_ead()
    asdf = 1