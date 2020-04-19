from typing import TypeVar, List

from instruments.Trade import Trade
from simm.Enums import ImRole
from simm.simmAPI import postCrif, calculateCrif
from utilities.Enums import Currency

A = TypeVar('A', Trade, List[Trade])
B = TypeVar('B', int, List[int])


class SIMM():

    def __init__(self):
        self.calculationCurrency = Currency.USD
        self.resultCurrency = Currency.USD
        self.imRole = ImRole.SECURED
        self.trades = []
        self.im = None
        self.upload_id = None
        self.calculated = False
        self.allocated = False

    def add_trades(self, trades: A):
        if type(trades) == list:
            self.trades += trades
        else:
            self.trades.append(trades)
        self.__resetCalculated__()

    def remove_trades(self, ids: B):
        if type(ids) == list:
            self.trades = [t for t in self.trades if t.id not in ids]
        else:
            self.trades = [t for t in self.trades if t.id is not ids]
        self.__resetCalculated__()

    def get_im(self):
        if self.calculated:
            return self.im

        crif = self.__createCrif__()
        self.upload_id = postCrif(crif)
        self.im = calculateCrif(self.upload_id, imRole=self.imRole, calculationCurrency=self.calculationCurrency,
                                resultCurrency=self.resultCurrency)
        self.calculated = True

    def __createCrif__(self):
        crif = []
        for t in self.trades:
            crif += t.get_simm_sensis()
        return crif

    def __resetCalculated__(self):
        self.im = None
        self.upload_id = None
        self.calculated = False
        self.allocated = False
