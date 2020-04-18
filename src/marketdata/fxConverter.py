from marketdata.fx_spot import FxSpot
from utilities.Enums import Currency


def fxConvert(fromCcy: Currency, toCcy: Currency, amount: float):
    ccyPair = fromCcy.name+toCcy.name
    return amount*FxSpot[ccyPair].value