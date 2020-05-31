from enum import Enum
from typing import Dict

from allocation.Enums import FdApproach, FdApproach2
from allocation.allocator import Allocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.Trade import Trade
from riskMeasureModel import RiskMeasureModel


class EulerAllocator(Allocator):

    def __init__(self, collateralAgreement: CollateralAgreement, normalization=False):
        super().__init__(collateralAgreement, normalization=normalization)
        self.rel_bumpsize = 0.0001
        self.abs_bumpsize = 0.01
        self.fdApproach = FdApproach.Relative
        self.fdApproach2 = FdApproach2.Forward

    def _temporarily_disable_mta(func):
        def wrapper(*args, **kwargs):
            mta = args[0].ca.mta
            args[0].ca.mta = 0
            result = func(*args, **kwargs)
            args[0].ca.mta = mta
            return result
        return wrapper

    @_temporarily_disable_mta
    def calculateTradeAllocation(self, model: RiskMeasureModel, trade: Trade) -> float:
        shifted_value = self.calculateShiftedValue(model, trade)
        if self.fdApproach == FdApproach.Relative:
            allocated_value = shifted_value / self.rel_bumpsize
        elif self.fdApproach == FdApproach.Absolute:
            allocated_value = trade.notional * (shifted_value/self.abs_bumpsize)
        return allocated_value

    def calculateShiftedValue(self, model:RiskMeasureModel, trade:Trade) -> float:
        orig_value = model.get_risk_measure()
        self.ca.remove_trades(trades=trade)
        if trade in model.trades:
            self.ca.add_trades(trade)
            raise (Exception(
                'Model you are trying to allocate is probably not synced with the used Collateral Agreement. Please make sure that e.g. sync_im_model parameter of the collateral agreement is set to True before running the allocation'))
        if self.fdApproach2 == FdApproach2.Forward:
            trade1 = trade.get_bumped_copy(rel_bump_size=self.rel_bumpsize, abs_bump_size=self.abs_bumpsize, bump_approach=self.fdApproach)
            trade2 = trade
        elif self.fdApproach2 == FdApproach2.Central:
            trade1 = trade.get_bumped_copy(rel_bump_size=(self.rel_bumpsize/2), abs_bump_size=(self.abs_bumpsize/2), bump_approach=self.fdApproach)
            trade2 = trade.get_bumped_copy(rel_bump_size=-(self.rel_bumpsize/2), abs_bump_size=-(self.abs_bumpsize/2), bump_approach=self.fdApproach)
        else: #self.fdAppraoch2 == FdApproach2.Backward
            trade1 = trade
            trade2 = trade.get_bumped_copy(rel_bump_size=-self.rel_bumpsize, abs_bump_size=-self.abs_bumpsize, bump_approach=self.fdApproach)

        if trade1 != trade:
            self.ca.add_trades(trade1)
            val1 = model.get_risk_measure()
            self.ca.remove_trades(trade1)
        else:
            val1 = orig_value

        if trade2 != trade:
            self.ca.add_trades(trade2)
            val2 = model.get_risk_measure()
            self.ca.remove_trades(trade2)
        else:
            val2 = orig_value

        self.ca.add_trades(trade)
        return val1-val2

    def shiftPortfolio(self, model: RiskMeasureModel) -> Dict[Trade, float]:
        shift = {}
        for t in model.trades:
            shift[t] = self.calculateShiftedValue(model, t)
        return shift

    def shift_ead(self) -> Dict[Trade, float]:
        return self.shiftPortfolio(self.ca.sa_ccr_model)

    def allocate_arbitrary_function(self, function):
        orig_value = function()
        allocation = {}
        for t in self.ca.trades:
            self.ca.remove_trades(t)
            bumpedtrade = t.get_bumped_copy(rel_bump_size=self.rel_bumpsize, abs_bump_size=self.abs_bumpsize, bump_approach=self.fdApproach)
            self.ca.add_trades(bumpedtrade)
            bumped_value = function()
            self.ca.remove_trades(trades=bumpedtrade)
            self.ca.add_trades(t)
            if self.fdApproach == FdApproach.Relative:
                allocation[t] = (bumped_value-orig_value) / self.rel_bumpsize
            elif self.fdApproach == FdApproach.Absolute:
                allocation[t] = t.notional * ((bumped_value-orig_value) / self.abs_bumpsize)

        return allocation