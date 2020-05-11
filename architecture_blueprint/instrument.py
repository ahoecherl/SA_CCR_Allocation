from typing import List, Dict


class Trade():

    def get_npv(self):
        #This is a lazy function that only recalculates the NPV using self.calculate_npv() if used marketdata has been changed since the last calculation.
        pass

    def get_simm_sensis(self):
        #This is a lazy function that only recalculates Sensitivities using self.calculate_simm_sensis() if used marketdata has been changed since the last calculation.
        pass

    def market_data_change(self):
        #Is called by linked marketdata if marketdata changes to inform the trade that recalcultion of NPV and SIMM is necessary if requested by one of the models.
        pass

    def calculate_simm_sensis(self):
        pass

    def calculate_npv(self):
        pass


class IRS(Trade):

    def __init__(self, notional, other_irs_parameters: Dict, marketdata : List[Marketdata]):
        super().__init__()
        for m in marketdata:
            m.link_observer()
        self.notional = notional
        self.other_irs_parameters = other_irs_parameters

    def calculate_simm_sensis(self, bumpsize):
        return self.calculate_simm_sensis_icurve(bumpsize) + self.calcualte_simm_sensis_fx




class Swaption(Trade):

    def __init__(self, underlying : IRS, other_swaption_parameters: Dict, marketdata_for_pricing : List[Marketdata]):