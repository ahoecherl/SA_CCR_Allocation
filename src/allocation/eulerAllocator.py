from typing import Dict

from allocation.allocator import Allocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.Trade import Trade
from genericRiskMeasureModel import GenericRiskMeasureModel


class EulerAllocator(Allocator):

    def __init__(self, collateralAgreement: CollateralAgreement):
        super().__init__(collateralAgreement)
        self.rel_bumpsize = 0.00001

    def __calculateTradeAllocation(self, model: GenericRiskMeasureModel, trade: Trade) -> float:
        orig_value = model.get_risk_measure()
        self.ca.remove_trades(trades=trade)
        if trade in model.trades:
            self.ca.add_trades(trade)
            raise (Exception(
                'Model you are trying to allocate is probably not synced with the used Collateral Agreement. Please make sure that e.g. sync_im_model parameter of the collateral agreement is set to True before running the allocation'))
        bumpedtrade = trade.get_bumped_copy(rel_bump_size=self.rel_bumpsize)
        self.ca.add_trades(bumpedtrade)
        bumped_value = model.get_risk_measure()
        self.ca.remove_trades(trades=bumpedtrade)
        self.ca.add_trades(trade)
        allocated_value = (bumped_value - orig_value) / self.rel_bumpsize
