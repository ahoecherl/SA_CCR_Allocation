import pytest
from pytest import approx

from collateralAgreement.collateralAgreement import CollateralAgreement, Margining, InitialMargining, Clearing
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from margining.simm import SIMM
from margining.noimm import NOIMM
from margining.variationMarginModel import VariationMarginModel, NoVariationMargin
from marketdata.EquitySpot import EquitySpot
from marketdata.fxConverter import fxConvert
from marketdata.interestRateIndices import InterestRateIndex
from sa_ccr.sa_ccr import SA_CCR
import QuantLib as ql
from marketdata import init_marketdata

from utilities.Enums import SwapDirection, Currency


def test_adding_and_removing_trades():
    ca = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    ca.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca))
    im_model = ca.get_im_model()
    vm_model = ca.get_vm_model()
    sa_ccr_model = ca.get_sa_ccr_model()

    assert isinstance(im_model, SIMM)
    assert isinstance(vm_model, VariationMarginModel)

    trade = IRS(notional=100, timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years),
                swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EURIBOR6M)

    ca.add_trades(trade)

    assert ca.trades == [trade]
    assert im_model.trades == [trade]
    assert vm_model.trades == [trade]
    assert sa_ccr_model.trades == [trade]

    trade2 = EquityOption(maturity=ql.Period(1, ql.Years))
    trade3 = EquityOption(maturity=ql.Period(2, ql.Years))

    ca.add_trades(trade2)
    ca.add_trades(trade3)
    ca.remove_trades(trades=trade)

    assert ca.trades == [trade2, trade3]
    assert im_model.trades == [trade2, trade3]
    assert vm_model.trades == [trade2, trade3]
    assert sa_ccr_model.trades == [trade2, trade3]


def test_adding_and_removing_trades_error_handling():
    trade = IRS(notional=100, timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years),
                swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EURIBOR6M)
    trade2 = EquityOption(maturity=ql.Period(1, ql.Years))
    trade3 = EquityOption(maturity=ql.Period(2, ql.Years))
    ca = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    ca.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca))
    ca.add_trades(trade)
    with pytest.raises(Exception):
        ca.add_trades(trade)
    ca.add_trades(trade2)
    with pytest.raises(Exception):
        ca.add_trades([trade3, trade3])
    ca.remove_trades(trade2)
    with pytest.raises(Exception):
        ca.add_trades([trade2, trade3, trade2])
    ca.add_trades(trade2)
    assert [trade, trade2] == ca.trades


def test_c_calculation():
    trade1 = EquityOption(maturity=ql.Period(1, ql.Years), strike=EquitySpot.ADS.value.value() - 5)
    trade = IRS(notional=100, timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years),
                swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EURIBOR6M, fixed_rate=0.00)

    ca_no_im = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.NO_IM)
    ca_no_im.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca_no_im))

    ca_no_im.add_trades([trade1, trade])
    assert ca_no_im.get_C() == ca_no_im.get_vm_model().get_vm() != 0

    ca_simm = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    ca_simm.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca_simm))

    ca_simm.add_trades([trade1, trade])
    assert 0 != ca_simm.get_C() != ca_simm.get_vm_model().get_vm() != 0
    assert ca_simm.get_C() - ca_simm.get_im_model().get_im_receive() == ca_simm.get_vm_model().get_vm()

    ca_ccp = CollateralAgreement(margining=Margining.MARGINED, clearing=Clearing.CLEARED,
                                 initialMargining=InitialMargining.CCPIMM)
    ca_ccp.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca_ccp))

    ca_ccp.add_trades([trade1, trade])
    assert ca_ccp.get_C() == ca_ccp.get_vm_model().get_vm() != 0

    ead_no_im = ca_no_im.get_sa_ccr_model().get_ead()
    ead_simm = ca_simm.get_sa_ccr_model().get_ead()
    ead_ccp = ca_ccp.get_sa_ccr_model().get_ead()

    assert ead_simm < ead_ccp < ead_no_im

    asdf = 1


def test_syncing_and_desyncing():
    ca = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    ca.link_sa_ccr_instance(SA_CCR(ca))

    trade1 = EquityOption(maturity=ql.Period(1, ql.Years), strike=EquitySpot.ADS.value.value() - 5)
    trade2 = IRS(notional=100, timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years),
                 swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.EURIBOR6M, fixed_rate=0.00)
    trade3 = IRS(notional=100, timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years),
                 swapDirection=SwapDirection.RECEIVER, index=InterestRateIndex.USDLIBOR3M, fixed_rate=0.01)

    ca.add_trades(trade1)
    ca.sync_im_model = False
    assert ca.vm_model.trades == [trade1]
    assert ca.im_model.trades == [trade1]
    ca.add_trades(trade2)
    assert ca.vm_model.trades == [trade1, trade2]
    assert ca.im_model.trades == [trade1]
    ca.sync_im_model = True
    assert ca.im_model.trades == [trade1, trade2]
    ca.add_trades(trade3)
    assert ca.vm_model.trades == [trade1, trade2, trade3]
    assert ca.im_model.trades == [trade1, trade2, trade3]

    # now check if the calculations also add up at least for VM

    ca = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.NO_IM)
    ca.link_sa_ccr_instance(SA_CCR(ca))

    npv_1 = fxConvert(trade1.currency, Currency.USD, trade1.get_price())
    npv_2 = fxConvert(trade2.currency, Currency.USD, trade2.get_price())
    npv_3 = fxConvert(trade3.currency, Currency.USD, trade3.get_price())

    ca.add_trades(trade1)
    ca.sync_vm_model = False
    assert ca.get_C() == ca.get_vm_model().get_vm() == npv_1 != 0
    ca.add_trades(trade2)
    assert ca.get_C() == npv_1
    ca.sync_vm_model = True
    assert ca.get_C() == npv_1 + npv_2
    ca.add_trades(trade3)
    assert ca.get_C() == npv_1 + npv_2 + npv_3

    # a few sanity checks for SA_CCR

    ca = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    local_sa_ccr_model = SA_CCR(ca)
    ca.link_sa_ccr_instance(local_sa_ccr_model)

    assert local_sa_ccr_model.get_ead() == 0
    ca.add_trades(trade1)
    ca.sync_im_model = False
    ca.sync_vm_model = False
    test_value = local_sa_ccr_model.get_ead()
    assert test_value > 0
    assert local_sa_ccr_model.trades == [trade1]
    ca.add_trades(trade2)
    test_value_2 = local_sa_ccr_model.get_ead()
    assert ca.vm_model.trades == [trade1]
    assert ca.im_model.trades == [trade1]
    ca.sync_vm_model = True
    ca.sync_im_model = True
    ca.sync_sa_ccr_model = True
    test_value_3 = local_sa_ccr_model.get_ead()
    assert test_value_2 != test_value_3
    assert local_sa_ccr_model.trades == [trade1, trade2]
    assert ca.vm_model.trades == [trade1, trade2]
    assert ca.im_model.trades == [trade1, trade2]
    ca.add_trades(trade3)
    test_value_4 = local_sa_ccr_model.get_ead()
    assert test_value_4 != test_value_3
    assert local_sa_ccr_model.trades == [trade1, trade2, trade3]
    assert ca.vm_model.trades == [trade1, trade2, trade3]
    assert ca.im_model.trades == [trade1, trade2, trade3]

def test_margining_switch():
    ca = CollateralAgreement(clearing=Clearing.UNCLEARED,margining=Margining.UNMARGINED, initialMargining=InitialMargining.NO_IM)
    ca.link_sa_ccr_instance(SA_CCR(ca))
    dummy_trade = EquityOption()
    ca.add_trades(dummy_trade)
    assert ca.initialMargining == InitialMargining.NO_IM
    assert ca.margining == Margining.UNMARGINED
    assert ca.clearing == Clearing.UNCLEARED
    assert ca.get_vm_model().__class__ == NoVariationMargin
    assert ca.get_im_model().__class__ == NOIMM

    with pytest.raises(Exception):
        ca.initialMargining = InitialMargining.SIMM
    with pytest.raises(Exception):
        ca.clearing = Clearing.CLEARED
    with pytest.raises(Exception):
        ca.initialMargining = InitialMargining.CCPIMM

    assert ca.get_vm_model().__class__ == NoVariationMargin
    assert ca.get_im_model().__class__ == NOIMM

    assert ca.get_C() == 0
    assert ca.get_C()-ca.get_V() < 0

    ca.margining = Margining.MARGINED
    assert ca.margining == Margining.MARGINED
    assert ca.initialMargining == InitialMargining.NO_IM
    assert ca.get_vm_model().__class__ == VariationMarginModel
    assert ca.get_C() > 0
    assert ca.get_C() - ca.get_V() == 0
    ca.initialMargining = InitialMargining.SIMM
    assert ca.margining == Margining.MARGINED
    assert ca.initialMargining == InitialMargining.SIMM
    assert ca.get_C() > 0
    assert ca.get_C() - ca.get_V() > 0

    assert ca.get_im_model().__class__ == SIMM

    with pytest.raises(Exception):
        ca.margining = Margining.UNMARGINED

    ca.initialMargining = InitialMargining.NO_IM
    ca.margining = Margining.UNMARGINED
    assert ca.margining == Margining.UNMARGINED
    assert ca.initialMargining == InitialMargining.NO_IM