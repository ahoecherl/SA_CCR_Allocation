from enum import Enum
import QuantLib as ql

from marketdata.interestRateCurves import OisCurve, LiborCurve

class InterestRateIndex(Enum):
    EONIA = ql.Eonia(OisCurve.EONIA.value)
    EURIBOR6M = ql.Euribor6M(LiborCurve.EURIBOR6M.value)
    USDLIBOR3M = ql.USDLibor(ql.Period(3, ql.Months), LiborCurve.USDLIBOR3M.value)
    FEDFUNDS = ql.FedFunds(OisCurve.FEDFUNDS.value)