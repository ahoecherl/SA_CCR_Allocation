from typing import TypeVar, List, Union

from instruments.Trade import Trade
from margining.Enums import ImRole
from margining.initialMarginModel import InitialMarginModel
from margining.simmAPI import postCrif, calculateCrif
from utilities.Enums import Currency

A = TypeVar('A', Trade, List[Trade])
B = TypeVar('B', int, List[int])


class SIMM(InitialMarginModel):

    def __init__(self, resultCurrency : Currency = Currency.USD):
        self.calculationCurrency = Currency.USD
        self.resultCurrency = resultCurrency
        self.trades = []
        self.im_receive = None
        self.im_post = None
        self.upload_id = None
        self.receive_calculated = False
        self.post_calculated = False
        self.allocated = False

    def get_im_receive(self):
        im_role = ImRole.SECURED
        if self.receive_calculated:
            return self.im_receive

        crif = self.__createCrif__()
        self.upload_id = postCrif(crif)
        self.im_receive = calculateCrif(self.upload_id, imRole=im_role, calculationCurrency=self.calculationCurrency,
                                        resultCurrency=self.resultCurrency)
        self.receive_calculated = True
        return self.im_receive

    def get_im_post(self):
        im_role = ImRole.PLEDGOR
        if self.post_calculated:
            return self.im_post

        crif = self.__createCrif__()
        self.upload_id = postCrif(crif)
        self.im_post = calculateCrif(self.upload_id, imRole=im_role, calculationCurrency=self.calculationCurrency,
                                        resultCurrency=self.resultCurrency)
        self.post_calculated = True
        return self.im_post

    def __createCrif__(self):
        crif = []
        for t in self.trades:
            crif += t.get_simm_sensis()
        return crif

    def __resetCalculated__(self):
        self.im_receive = None
        self.im_post = None
        self.upload_id = None
        self.receive_calculated = False
        self.post_calculated = False
        self.allocated = False
