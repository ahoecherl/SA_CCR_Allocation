import inspect
import warnings
from typing import List, Union

from instruments.Trade import Trade


class TradeContainerInterface:

    def add_trades(self, trades: Union[Trade, List[Trade]]):
        from collateralAgreement.collateralAgreement import CollateralAgreement
        if not isinstance(self, CollateralAgreement):
            # Potential warning as this should only be manipulated directly in CollateralAgreementClass to preserve consistency
            stack = inspect.stack()
            if not isinstance(stack[1][0].f_locals['self'], CollateralAgreement):
                warnings.warn('This should only be directly called on Collateral Agreement to make certain that trades stay consistent between Col Agreement, SA-CCR Model, VM Model and IM Model')

        if type(trades) == list:
            self.trades += trades
        else:
            self.trades.append(trades)

    def remove_trades(self, trade_ids: Union[None, int, List[int]] = None, trades: Union[None, Trade, List[Trade]] = None):
        from collateralAgreement.collateralAgreement import CollateralAgreement
        if not isinstance(self, CollateralAgreement):
            # Potential warning as this should only be manipulated directly in CollateralAgreementClass to preserve consistency
            stack = inspect.stack()
            if not isinstance(stack[1][0].f_locals['self'], CollateralAgreement):
                warnings.warn('This should only be directly called on Collateral Agreement to make certain that trades stay consistent between Col Agreement, SA-CCR Model, VM Model and IM Model')

        if trade_ids is not None:
            if isinstance(trade_ids, int):
                trade_ids = [trade_ids]
            self.trades = [t for t in self.trades if t.id not in trade_ids]
        if trades is not None:
            if isinstance(trades, Trade):
                trades = [trades]
            self.trades = [t for t in self.trades if t not in trades]