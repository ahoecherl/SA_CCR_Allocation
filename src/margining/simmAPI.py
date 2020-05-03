import requests
import ast
import pprint
from typing import List, Dict

from margining.Enums import ImRole
from utilities.Enums import Currency

home = 'http://localhost:8080/'


def __checkError__(r: requests.Response):
    if r.status_code != 200:
        raise ConnectionError(pprint.pprint(ast.literal_eval(r.text)))


def postCrif(crif: List[Dict]) -> int:
    loc = 'crifs'
    r = requests.post(home + loc, json=crif)
    __checkError__(r)
    return int(r.content)


def getCrif(id: int):
    loc = 'crifs/%d' % id
    r = requests.get(home + loc)
    __checkError__(r)
    return ast.literal_eval(r.content.decode())


def calculateCrif(id: int, imRole: ImRole = ImRole.SECURED, calculationCurrency: Currency = Currency.USD,
                  resultCurrency: Currency = Currency.USD) -> List[Dict]:
    loc = 'crifs/%d/calculate' % id
    params = {'imRole': imRole.value, 'calculationCurrency': calculationCurrency.value, 'resultCurrency': resultCurrency.value}
    r = requests.get(home + loc, params=params)
    __checkError__(r)
    return float(r.content.decode())
