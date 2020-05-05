import pytest

from allocation.incrementalAllocator import IncrementalAllocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from sa_ccr.sa_ccr import SA_CCR
from test_fixtures import init_ca




def test_for_smoke(init_ca):
    ca = init_ca
    incrementalAllocator = IncrementalAllocator(ca)
    allocated_vm = incrementalAllocator.allocate_vm()
    allocated_im = incrementalAllocator.allocate_im()
    allocated_ead = incrementalAllocator.allocate_ead()
    asdf = 1


def test_exception(init_ca: CollateralAgreement):
    ca = init_ca
    incrementalAllocator = IncrementalAllocator(ca)
    allocated_vm = incrementalAllocator.allocate_vm()
    ca.sync_vm_model = False
    with pytest.raises(Exception):
        assert incrementalAllocator.allocate_vm()

    allocated_im = incrementalAllocator.allocate_im()
    ca.sync_im_model = False
    with pytest.raises(Exception):
        assert incrementalAllocator.allocate_im()

    allocated_ead = incrementalAllocator.allocate_ead()
    ca.sync_sa_ccr_model = False
    with pytest.raises(Exception):
        assert incrementalAllocator.allocate_ead()

    asdf =1