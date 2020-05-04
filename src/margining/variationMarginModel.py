from margining.marginModel import MarginModel
from marketdata.fxConverter import fxConvert
from utilities.Enums import Currency


class VariationMarginModel(MarginModel):

    def __init__(self, vm_currency: Currency = Currency.USD):
        self.trades = []
        self.vm_currency = vm_currency

    def get_vm(self):
        vm = 0
        for t in self.trades:
            vm += fxConvert(fromCcy=t.currency, toCcy=self.vm_currency, amount=t.get_price())
        return vm

    def get_risk_measure(self):
        return self.get_vm()


class NoVariationMargin(VariationMarginModel):

    def get_vm(self):
        return 0
