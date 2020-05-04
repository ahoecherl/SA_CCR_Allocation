from plistlib import Dict

from collateralAgreement.collateralAgreement import CollateralAgreement
from instruments.Trade import Trade
from genericRiskMeasureModel import GenericRiskMeasureModel


class Allocator:

    def __init__(self, collateralAgreement: CollateralAgreement):
        self.ca = collateralAgreement

    def __allocatePortfolio(self, model: GenericRiskMeasureModel) -> Dict[Trade: float]:
        result = {}
        for t in model.trades:
            result[t] = self.__calculateTradeAllocation(model, t)
        return result

    def __calculateTradeAllocation(self, model: GenericRiskMeasureModel, trade: Trade) -> float:
        pass

    def allocate_vm(self) -> Dict[Trade: float]:
        return self.__allocatePortfolio(self.ca.vm_model)

    def allocate_im(self) -> Dict[Trade: float]:
        return self.__allocatePortfolio(self.ca.im_model)

    def allocate_ead(self) -> Dict[Trade: float]:
        return self.__allocatePortfolio(self.ca.sa_ccr_model)

