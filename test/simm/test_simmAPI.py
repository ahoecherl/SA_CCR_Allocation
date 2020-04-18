import pytest
from simm.simmAPI import postCrif,getCrif

testCrifOneLine = [{
        "tradeId": "TestTrade1",
        "imModel": "SIMM",
        "productClass": "RatesFx",
        "riskType": "Risk_FX",
        "qualifier": "CHF",
        "bucket": "",
        "label1": "",
        "label2": "",
        "amount": "200",
        "amountCurrency": "EUR",
        "amountUSD": "220",
        "postRegulation": "",
        "collectRegulation": "",
        "valuationDate": "2019-10-22",
        "endDate": "",
        "notional": "",
        "notionalCurrency": "",
        "notionalString": ""
    }]

corruptedCrif = [{
        "tradeId": "TestTrade1",
        "immModel": "SIMM",
        "productClass": "RatesFx",
        "riskType": "Risk_FX",
        "qualifier": "CHF",
        "bucket": "",
        "label1": "",
        "label2": "",
        "amount": "200",
        "amountCurrency": "EUR",
        "amountUSD": "220",
        "postRegulation": "",
        "collectRegulation": "",
        "valuationDate": "2019-10-22",
        "endDate": "",
        "notional": "",
        "notionalCurrency": "",
        "notionalString": ""
    }]

testCrifMultiLine = [
    {
        "tradeId": "TestTrade1",
        "imModel": "SIMM",
        "productClass": "RatesFx",
        "riskType": "Risk_FX",
        "qualifier": "CHF",
        "bucket": "",
        "label1": "",
        "label2": "",
        "amount": "200",
        "amountCurrency": "EUR",
        "amountUSD": "220",
        "postRegulation": "",
        "collectRegulation": "",
        "valuationDate": "2019-10-22",
        "endDate": "",
        "notional": "",
        "notionalCurrency": "",
        "notionalString": ""
    },
    {
        "tradeId": "TestTrade2",
        "imModel": "SIMM",
        "productClass": "RatesFx",
        "riskType": "Risk_FX",
        "qualifier": "CLP",
        "bucket": "",
        "label1": "",
        "label2": "",
        "amount": "100",
        "amountCurrency": "EUR",
        "amountUSD": "110",
        "postRegulation": "",
        "collectRegulation": "",
        "valuationDate": "2019-10-22",
        "endDate": "",
        "notional": "",
        "notionalCurrency": "",
        "notionalString": ""
    }
]

def test_postCrif():
    crif_id = postCrif(testCrifMultiLine)

@pytest.mark.skip(reason='Test case not yet finished')
def test_postCrif_error():
    crif_id = postCrif({'error':'error'})


def test_getCrif():
    id = 0
    getCrif(id)