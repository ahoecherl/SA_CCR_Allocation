import requests
import ast
import pprint
from typing import List, Dict

home = 'http://localhost:8080/'

def __checkError__(r: requests.Response):
    if r.status_code!=200:
        raise ConnectionError(pprint.pprint(ast.literal_eval(r.text)))


def postCrif(crif: List[Dict]) -> int:
    loc = 'crifs'
    r = requests.post(home+loc, json=crif)
    __checkError__(r)
    return int(r.content)

def getCrif(id: int):
    loc = 'crifs/'
    r = requests.get(home+loc+str(id))
