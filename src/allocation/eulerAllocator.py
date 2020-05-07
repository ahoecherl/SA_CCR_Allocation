from enum import Enum
from typing import Dict

from allocation.Enums import FdApproach
from allocation.allocator import Allocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.Trade import Trade
from genericRiskMeasureModel import GenericRiskMeasureModel


class EulerAllocator(Allocator):

    def __init__(self, collateralAgreement: CollateralAgreement, normalization=False):
        super().__init__(collateralAgreement, normalization=normalization)
        self.rel_bumpsize = 0.00001
        self.abs_bumpsize = 0.01
        self.fdApproach = FdApproach.Relative

    def calculateTradeAllocation(self, model: GenericRiskMeasureModel, trade: Trade) -> float:
        shifted_value = self.calculateShiftedValue(model, trade)
        if self.fdApproach == FdApproach.Relative:
            allocated_value = shifted_value / self.rel_bumpsize
        elif self.fdApproach == FdApproach.Absolute:
            allocated_value = trade.notional * (shifted_value / self.abs_bumpsize)
        return allocated_value

    def calculateShiftedValue(self, model:GenericRiskMeasureModel, trade:Trade) -> float:
        orig_value = model.get_risk_measure()
        self.ca.remove_trades(trades=trade)
        if trade in model.trades:
            self.ca.add_trades(trade)
            raise (Exception(
                'Model you are trying to allocate is probably not synced with the used Collateral Agreement. Please make sure that e.g. sync_im_model parameter of the collateral agreement is set to True before running the allocation'))
        bumpedtrade = trade.get_bumped_copy(rel_bump_size=self.rel_bumpsize, abs_bump_size=self.abs_bumpsize, bump_approach=self.fdApproach)
        self.ca.add_trades(bumpedtrade)
        bumped_value = model.get_risk_measure()
        self.ca.remove_trades(trades=bumpedtrade)
        self.ca.add_trades(trade)
        return bumped_value-orig_value

    def shiftPortfolio(self, model: GenericRiskMeasureModel) -> Dict[Trade, float]:
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



