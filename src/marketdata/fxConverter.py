from marketdata.fx_spot import FxSpot
from utilities.Enums import Currency


def fxConvert(fromCcy: Currency, toCcy: Currency, amount: float):
    if fromCcy == toCcy:
        return amount
    ccyPair = fromCcy.name+toCcy.name
    return amount*FxSpot[ccyPair].value