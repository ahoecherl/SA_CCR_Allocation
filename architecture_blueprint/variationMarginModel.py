from architecture_blueprint.riskMeasureModel import RiskMeasureModel


class VariationMarginModel(RiskMeasureModel):
    # Used if exchange of variation margin is mandated by the connected collateral agreement
    def __init__(self, marginCurrency):
        super().__init__()
        self.marginCurrency = marginCurrency

    def calculate_risk_measure(self):
        portfolio_npv = self.portfolio.get_NPV()
        self.vm = fxConvert(fromCcy=BankRiskCcy, toCcy=self.marginCurrency, amount=portfolio_npv)
        return self.vm


class NoVariationMargin(VariationMarginModel):
    # Used if no exchange of variation margin is mandated
    def get_vm(self):
        return 0
