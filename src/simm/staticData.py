import QuantLib as ql

from simm.Enums import SimmTenor

indexToLabel2 = {'EONIA':'OIS',
                 'USDLIBOR3M': 'Libor3m',
                 'EURIBOR6M': 'Libor6m',
                 'FEDFUNDS': 'OIS'}

def periodToLabel1(period: ql.Period) -> str:
    return SimmTenor[period]