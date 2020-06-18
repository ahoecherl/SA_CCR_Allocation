from typing import Union, List

from instruments.Trade import Trade


class Portfolio:

    def add_trades(self, trades: Union[Trade, List[Trade]]):
        if isinstance(trades, Trade):
            trades = [trades]
        if len(trades) > len(set(trades)):
            raise(Exception('There are duplicates within the list of trades you want to add. No duplicates are allowed in the list of trades - you have to create individual objects.'))
        s1 = set(self.trades)
        s2 = set(trades)
        if s1.intersection(s2):
            raise (Exception(
                'One or multiple of the trades you are trying to add are duplicates. This is forbidden.'))
        self.trades += trades

    def remove_trades(self, trades: Union[None, Trade, List[Trade]] = None):
        if isinstance(trades, Trade):
            trades = [trades]
        self.trades = [t for t in self.trades if t not in trades]

    def remove_all_trades(self):
        self.trades = []

    def replace_trade(self, trade_to_be_replaced: Trade, replacement_trade: Trade):
        self.remove_trades(trade_to_be_replaced)
        self.add_trades(replacement_trade)
