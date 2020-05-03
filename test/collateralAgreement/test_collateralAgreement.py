import pytest

from collateralAgreement.collateralAgreement import CollateralAgreement, Margining, InitialMargining, Clearing
from instruments.equity_instruments.equityOption import EquityOption
from instruments.interestRateInstrument.irs import IRS
from margining.simm import SIMM
from margining.variationMarginModel import VariationMarginModel
from marketdata.EquitySpot import EquitySpot
from marketdata.interestRateIndices import InterestRateIndex
from sa_ccr.sa_ccr import SA_CCR
import QuantLib as ql
from marketdata import init_marketdata

from utilities.Enums import SwapDirection


def test_adding_and_removing_trades():
    ca = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    ca.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca))
    im_model = ca.get_im_model()
    vm_model = ca.get_vm_model()
    sa_ccr_model = ca.get_sa_ccr_model()

    assert isinstance(im_model, SIMM)
    assert isinstance(vm_model, VariationMarginModel)

    trade = IRS(notional=100,timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years), swapDirection=SwapDirection.RECEIVER, index = InterestRateIndex.EURIBOR6M)

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


def test_c_calculation():
    trade1 = EquityOption(maturity=ql.Period(1, ql.Years), strike=EquitySpot.ADS.value.value()-5)
    trade = IRS(notional=100,timeToSwapStart=ql.Period(2, ql.Days), timeToSwapEnd=ql.Period(1, ql.Years), swapDirection=SwapDirection.RECEIVER, index = InterestRateIndex.EURIBOR6M, fixed_rate=0.00)

    ca_no_im = CollateralAgreement(margining=Margining.MARGINED)
    ca_no_im.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca_no_im))

    ca_no_im.add_trades([trade1, trade])
    assert ca_no_im.get_C() == ca_no_im.get_vm_model().get_vm() != 0

    ca_simm = CollateralAgreement(margining=Margining.MARGINED, initialMargining=InitialMargining.SIMM)
    ca_simm.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca_simm))

    ca_simm.add_trades([trade1, trade])
    assert 0 != ca_simm.get_C() != ca_simm.get_vm_model().get_vm() != 0
    assert ca_simm.get_C()-ca_simm.get_im_model().get_im_receive() == ca_simm.get_vm_model().get_vm()

    ca_ccp = CollateralAgreement(margining=Margining.MARGINED,clearing=Clearing.CLEARED, initialMargining=InitialMargining.CCPIMM)
    ca_ccp.link_sa_ccr_instance(SA_CCR(collateralAgreement=ca_ccp))

    ca_ccp.add_trades([trade1, trade])
    assert ca_ccp.get_C() == ca_ccp.get_vm_model().get_vm() != 0

    ead_no_im = ca_no_im.get_sa_ccr_model().get_ead()
    ead_simm = ca_simm.get_sa_ccr_model().get_ead()
    ead_ccp = ca_ccp.get_sa_ccr_model().get_ead()

    assert ead_simm < ead_ccp < ead_no_im

    asdf = 1