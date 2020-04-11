import pytest
from test.test_fixtures import *
from marketdata.interestRateCurves import LiborCurve, OisCurve


def test_EONIA(initialize_test):
    OisCurve.EONIA.value

def test_EURIBOR6M(initialize_test):
    LiborCurve.EURIBOR6M.value

def test_FEDFUNDS(initialize_test):
    OisCurve.FEDFUNDS.value

def test_USDLIBOR3M(initialize_test):
    LiborCurve.USDLIBOR3M.value