from typing import Union, List

from instruments.Trade import Trade
from margining.marginModel import MarginModel
from utilities.Enums import Currency


class InitialMarginModel(MarginModel):

    def __init__(self, resultCurrency : Currency = Currency.USD):
        self.resultCurrency = resultCurrency
        self.trades=[]

    def add_trades(self, trades: Union[Trade, List[Trade]]):
        super().add_trades(trades)
        self.__resetCalculated__()

    def remove_trades(self, trades: Union[None, Trade, List[Trade]] = None):
        super().remove_trades(trades=trades)
        self.__resetCalculated__()

    def __resetCalculated__(self):
        pass

    def get_im_post(self):
        pass

    def get_im_receive(self):
        pass

    def get_risk_measure(self):
        return self.get_im_receive()
