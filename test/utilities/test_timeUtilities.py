from utilities.timeUtilities import *
import pytest

def test_convert_period_to_days():
    assert 60 == convert_period_to_days(ql.Period(60, ql.Days))
    assert 60 == convert_period_to_days(ql.Period(2, ql.Months))
    assert 720 == convert_period_to_days(ql.Period(2, ql.Years))