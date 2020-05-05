import pytest

from allocation.eulerAllocator import EulerAllocator
from allocation.proRataAllocator import ProRataAllocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from sa_ccr.sa_ccr import SA_CCR
from test_fixtures import init_ca


def test_for_smoke(init_ca: CollateralAgreement):
    ca = init_ca
    proRataAllocator = ProRataAllocator(ca)
    allocated_vm = proRataAllocator.allocate_vm()
    allocated_im = proRataAllocator.allocate_im()
    allocated_ead = proRataAllocator.allocate_ead()
    asdf = 1


def test_exception(init_ca: CollateralAgreement):
    ca = init_ca
    proRataAllocator = ProRataAllocator(ca)
    allocated_vm = proRataAllocator.allocate_vm()
    ca.sync_vm_model = False
    with pytest.raises(Exception):
        assert proRataAllocator.allocate_vm()

    allocated_im = proRataAllocator.allocate_im()
    ca.sync_im_model = False
    with pytest.raises(Exception):
        assert proRataAllocator.allocate_im()

    allocated_ead = proRataAllocator.allocate_ead()
    ca.sync_sa_ccr_model = False
    with pytest.raises(Exception):
        assert proRataAllocator.allocate_ead()

    asdf =1