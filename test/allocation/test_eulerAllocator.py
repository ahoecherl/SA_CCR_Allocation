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
from test_fixtures import init_ca


def test_for_smoke(init_ca: CollateralAgreement):
    ca = init_ca
    eulerAllocator = EulerAllocator(ca)
    allocated_vm = eulerAllocator.allocate_vm()
    allocated_im = eulerAllocator.allocate_im()
    allocated_ead = eulerAllocator.allocate_ead()
    ca.sync_im_model = False
    ca.sync_vm_model = False
    allocated_ead2 = eulerAllocator.allocate_ead()
    

    asdf = 1

def test_exception(init_ca: CollateralAgreement):
    ca = init_ca
    eulerAllocator = EulerAllocator(ca)
    allocated_vm = eulerAllocator.allocate_vm()
    ca.sync_vm_model = False
    with pytest.raises(Exception):
        assert eulerAllocator.allocate_vm()

    allocated_im = eulerAllocator.allocate_im()
    ca.sync_im_model = False
    with pytest.raises(Exception):
        assert eulerAllocator.allocate_im()

    allocated_ead = eulerAllocator.allocate_ead()
    ca.sync_sa_ccr_model = False
    with pytest.raises(Exception):
        assert eulerAllocator.allocate_ead()

    asdf =1