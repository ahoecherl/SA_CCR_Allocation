import pytest
import QuantLib as ql

from test.test_fixtures import *
from marketdata.interestRateCurves import LiborCurve, OisCurve
from marketdata.interestRateIndices import InterestRateIndex
from marketdata.util import today


def test_manual_creation_from_marketdata(initialize_test):

    nominal = 1.0
    fixedRate = 0.00
    dc = ql.Actual360()
    type = ql.OvernightIndexedSwap.Payer
    test_schedule = ql.Schedule(ql.TARGET().advance(today, 2, ql.Days), ql.Date(11, ql.May, 2020), ql.Period(1, ql.Years), ql.TARGET(),
                                ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False)
    test_ois = ql.OvernightIndexedSwap(type, nominal, test_schedule, fixedRate, dc, InterestRateIndex.EONIA.value)

    test_ois.setPricingEngine(ql.DiscountingSwapEngine(OisCurve.EONIA.value))

    test_ois.fairRate()
    test_ois.NPV()