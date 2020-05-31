import pytest
import QuantLib as ql
from pytest import approx

from allocation.Enums import FdApproach, FdApproach2
from allocation.eulerAllocator import EulerAllocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from marketdata import init_marketdata
from sa_ccr.sa_ccr import SA_CCR
from test_fixtures import init_ca
from utilities.Enums import SwapDirection


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


def test_allocate_arbitrary_function(init_ca: CollateralAgreement):
    ca = init_ca
    eulerAllocator = EulerAllocator(ca)
    multiplierAllocation = eulerAllocator.allocate_arbitrary_function(ca.get_sa_ccr_model().get_multiplier)
    asfd = 1


def test_allocate_with_absolute_shift(init_ca: CollateralAgreement):
    eA_abs = EulerAllocator(init_ca)
    eA_abs.fdApproach = FdApproach.Absolute
    ead_allocation_abs = eA_abs.allocate_ead()
    assert approx(eA_abs.subadditivity_check_ead(ead_allocation_abs), abs = 0.01) == 0
    eA_rel = EulerAllocator(init_ca)
    eA_rel.fdApproach = FdApproach.Relative
    ead_allocation_rel = eA_abs.allocate_ead()
    assert approx(eA_abs.subadditivity_check_ead(ead_allocation_abs), abs = 0.01) == 0

def test_temporarily_disable_mta():
    ca_with_mta = CollateralAgreement(mta=1000000,
                             threshold=0)
    ca_with_mta.link_sa_ccr_instance(SA_CCR(ca_with_mta))
    ca_no_mta = CollateralAgreement(mta=0,
                                    threshold=0)
    ca_no_mta.link_sa_ccr_instance(SA_CCR(ca_no_mta))
    trade = IRS(notional = 100000000)
    ca_with_mta.add_trades(trade)
    ca_no_mta.add_trades(trade)

    allocator_with_mta = EulerAllocator(ca_with_mta)
    allocator_no_mta = EulerAllocator(ca_no_mta)
    with_mta = allocator_with_mta.allocate_ead()[trade]
    no_mta = allocator_no_mta.allocate_ead()[trade]
    assert pytest.approx(with_mta, rel=0.00001) == no_mta not in [None, 0]

def test_central_forward_backward_difference():
    IRS1 = IRS(swapDirection=SwapDirection.PAYER)
    IRS2 = IRS(swapDirection=SwapDirection.RECEIVER)
    ca = CollateralAgreement()
    ca.link_sa_ccr_instance(SA_CCR(ca))
    ca.add_trades([IRS1, IRS2])
    allocator = EulerAllocator(ca)
    forward = allocator.allocate_im()
    allocator.fdApproach2 = FdApproach2.Forward
    forward2 = allocator.allocate_im()
    assert forward == forward2
    allocator.fdApproach2 = FdApproach2.Central
    central = allocator.allocate_im()
    allocator.fdApproach2 = FdApproach2.Backward
    backward = allocator.allocate_im()

    assert approx(central[IRS1], abs=0.01) == 0
    assert approx(central[IRS2], abs=0.01) == 0
    assert approx(forward[IRS1], abs=0.1) != 0
    assert approx(backward[IRS2], abs=0.1) != 0
    assert approx(forward[IRS1], rel=0.01) == -backward[IRS1]
    assert approx(forward[IRS2], rel=0.01) == -backward[IRS2]

    asdf = 1