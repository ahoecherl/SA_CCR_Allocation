from allocation.allocator import Allocator
from collateralAgreement.collateralAgreement import CollateralAgreement
from genericRiskMeasureModel import GenericRiskMeasureModel
from instruments.Trade import Trade


class ProRataAllocator(Allocator):

    def __init__(self, collateralAgreement: CollateralAgreement, normalization: bool = True):
        super().__init__(collateralAgreement=collateralAgreement, normalization=normalization)

    def calculateTradeAllocation(self, model: GenericRiskMeasureModel, trade: Trade) -> float:
        backup_trades = self.ca.trades
        self.ca.remove_all_trades()
        if model.trades != []:
            self.ca.add_trades(backup_trades)
            raise (Exception(
                'Model you are trying to allocate is probably not synced with the used Collateral Agreement. Please make sure that e.g. sync_im_model parameter of the collateral agreement is set to True before running the allocation'))
        self.ca.add_trades(trade)
        allocated_value = model.get_risk_measure()
        self.ca.remove_all_trades()
        self.ca.add_trades(backup_trades)
        return allocated_value
