from typing import Dict

from allocation.allocator import Allocator
from genericRiskMeasureModel import GenericRiskMeasureModel
from instruments.Trade import Trade


class IncrementalAllocator(Allocator):

    def allocatePortfolio(self, model: GenericRiskMeasureModel) -> Dict[Trade, float]:
        allocation = {}
        trades = self.ca.trades
        self.ca.remove_all_trades()
        if model.trades != []:
            self.ca.add_trades(trades)
            raise (Exception(
                'Model you are trying to allocate is probably not synced with the used Collateral Agreement. Please make sure that e.g. sync_im_model parameter of the collateral agreement is set to True before running the allocation'))
        for t in trades:
            if not model.trades: #Checking if the list is empty
                pre_measure = 0
            else:
                pre_measure = model.get_risk_measure()
            self.ca.add_trades(t)
            post_measure = model.get_risk_measure()
            inc_measure = post_measure-pre_measure
            allocation[t] = inc_measure
        return allocation

