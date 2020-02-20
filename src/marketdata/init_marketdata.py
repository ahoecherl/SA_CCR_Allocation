import QuantLib as ql
from marketdata.util import today, testVar2

ql.Settings.instance().evaluationDate = today

testVar = 3