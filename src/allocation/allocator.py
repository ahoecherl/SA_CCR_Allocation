from typing import Dict

from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.Trade import Trade
from genericRiskMeasureModel import GenericRiskMeasureModel


class Allocator:

    def __init__(self, collateralAgreement: CollateralAgreement, normalization: bool = False):
        self.ca = collateralAgreement
        self.normalization = normalization

    def allocatePortfolio(self, model: GenericRiskMeasureModel) -> Dict[Trade, float]:
        allocation = {}
        for t in model.trades:
            allocation[t] = self.calculateTradeAllocation(model, t)
        if self.normalization:
            allocation = self.normalizeAllocation(allocation, model.get_risk_measure())
        return allocation

    def normalizeAllocation(self, allocation: Dict[Trade, float], risk_measure: float) -> Dict[Trade, float]:
        sum = 0
        for val in allocation.values():
            sum += val
        factor = risk_measure / sum
        for key, val in allocation.items():
            allocation[key] = val * factor
        return allocation

    def calculateTradeAllocation(self, model: GenericRiskMeasureModel, trade: Trade) -> float:
        pass

    def allocate_vm(self) -> Dict[Trade, float]:
        return self.allocatePortfolio(self.ca.vm_model)

    def allocate_im(self) -> Dict[Trade, float]:
        return self.allocatePortfolio(self.ca.im_model)

    def allocate_ead(self) -> Dict[Trade, float]:
        return self.allocatePortfolio(self.ca.sa_ccr_model)

    def subadditivity_check_ead(self, allocation: Dict[Trade, float]):
        return sum([v for v in allocation.values()]) - self.ca.sa_ccr_model.get_risk_measure()

