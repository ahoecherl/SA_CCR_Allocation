import inspect
import warnings
from typing import List, Union

from instruments.Trade import Trade


class GenericRiskMeasureModel:

    def add_trades(self, trades: Union[Trade, List[Trade]]):

        if type(trades) == list:
            self.trades += trades
        else:
            self.trades.append(trades)

    def remove_trades(self, trade_ids: Union[None, int, List[int]] = None, trades: Union[None, Trade, List[Trade]] = None):

        if trade_ids is not None:
            if isinstance(trade_ids, int):
                trade_ids = [trade_ids]
            self.trades = [t for t in self.trades if t.id not in trade_ids]
        if trades is not None:
            if isinstance(trades, Trade):
                trades = [trades]
            self.trades = [t for t in self.trades if t not in trades]

    def remove_all_trades(self):
        self.trades = []

    def get_risk_measure(self):
        pass