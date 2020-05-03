from math import sqrt

from margining.Enums import ImRole
from margining.initialMarginModel import InitialMarginModel
from margining.simm import SIMM
from utilities.Enums import Currency, AssetClass


class CCPIMM(InitialMarginModel):
    equity_holding_period = 3
    irs_holding_period = 5
    bilateral_holding_period = 10


    def __init__(self, resultCurrency: Currency = Currency.USD):
        self.calculationCurrency = Currency.USD
        self.resultCurrency = resultCurrency
        self.trades = []
        self.im_receive = 0
        self.im_post = None
        self.equity_model = None
        self.irs_model = None
        self.receive_calculated = True
        self.post_calculated = False
        self.allocated = False

    def get_im_post(self):
        im_role = ImRole.PLEDGOR
        if self.post_calculated:
            return self.im_post
        equity_trades = []
        irs_trades = []
        for t in self.trades:
            if t.assetClass == AssetClass.EQ:
                equity_trades.append(t)
            elif t.assetClass == AssetClass.IR:
                irs_trades.append(t)
            else:
                raise(Exception('can only handle equity and interest rate trades'))
        self.equity_model = SIMM()
        self.irs_model = SIMM()
        self.equity_model.add_trades(equity_trades)
        self.irs_model.add_trades(irs_trades)
        eq_im_post = self.equity_model.get_im_post()*sqrt(CCPIMM.equity_holding_period/CCPIMM.bilateral_holding_period)
        irs_im_post = self.irs_model.get_im_post() * sqrt(
            CCPIMM.irs_holding_period / CCPIMM.bilateral_holding_period)
        self.im_post = eq_im_post+irs_im_post
        return self.im_post

    def get_im_receive(self):
        return self.im_receive



    def __resetCalculated__(self):
        self.im_post = None
        self.equity_model = None
        self.irs_model = None
        self.post_calculated = False
        self.allocated = False
