import json
from enum import Enum
from typing import Union, List

from instruments.Trade import Trade
from margining.ccpimm import CCPIMM
from margining.noimm import NOIMM
from margining.simm import SIMM
from margining.variationMarginModel import NoVariationMargin, VariationMarginModel
from tradeContainerInterface import TradeContainerInterface
from utilities.Enums import Currency


class Margining(Enum):
    MARGINED = 'Margined'
    UNMARGINED = 'Unmargined'


class InitialMargining(Enum):
    NO_IM = 'No IM is exchanged bilaterally'
    SIMM = 'IM is exchanges bilaterally and calculated with SIMM'
    CCPIMM = 'IM is posted to a CCP'


class Tradecount(Enum):
    UNDER_FIVE_THOUSAND = 'Under five thousand transactions between the counterparties'
    OVER_FIVE_THOUSAND = 'Five thousand or more transactions between the counterparties (sadly not 9000)'


class Clearing(Enum):
    UNCLEARED = 'Non-centrally cleared derivatives'
    CLEARED = 'Centrally cleared derivatives'


class Dispute(Enum):
    NO_OUTSTANDING_DISPUTES = 'No margining disputes are outstanding between the counterparties'
    OUTSTANDING_DISPUTES = 'Disputes are outstanding between the counterparties'


class CollateralAgreement(TradeContainerInterface):

    def __init__(self,
                 margining: Margining = Margining.UNMARGINED,
                 clearing: Clearing = Clearing.UNCLEARED,
                 initialMargining: InitialMargining = InitialMargining.NO_IM,
                 tradecount: Tradecount = Tradecount.UNDER_FIVE_THOUSAND,
                 dispute: Dispute = Dispute.NO_OUTSTANDING_DISPUTES,
                 margin_currency: Currency = Currency.USD,
                 threshold: float = 0.0,
                 mta: float = 0.0,
                 unsegregated_overcollateraliziation_posted: float = 0.0,
                 unsegregated_overcollateralization_received: float = 0.0,
                 segregated_overcollateralization_posted: float = 0.0,
                 segregated_overcollateralization_received: float = 0.0):
        self.trades = []
        self.margining = margining
        self.clearing = clearing
        self.initialMargining = initialMargining
        self.margin_currency = margin_currency
        self.tradecount = tradecount
        self.dispute = dispute
        self.threshold = threshold
        self.mta = mta
        self.unsegregated_overcollateraliziation_posted = unsegregated_overcollateraliziation_posted
        self.unsegregated_overcollateralization_received = unsegregated_overcollateralization_received
        self.segregated_overcollateralization_posted = segregated_overcollateralization_posted
        self.segregated_overcollateralization_received = segregated_overcollateralization_received
        if margining == Margining.UNMARGINED and not (
                clearing == Clearing.UNCLEARED and initialMargining == InitialMargining.NO_IM):
            raise (Exception('No IM can be exhchanged for an unmargined collateral agreement '))
        if clearing == Clearing.CLEARED and not initialMargining == InitialMargining.CCPIMM:
            raise (Exception('If the collateral agreement is cleared CCPIMM has to be used as the IM Model'))
        if margining == Margining.UNMARGINED:
            self.vm_model = NoVariationMargin()
        elif margining == Margining.MARGINED:
            self.vm_model = VariationMarginModel(vm_currency=margin_currency)
        if initialMargining == InitialMargining.CCPIMM:
            self.im_model = CCPIMM(resultCurrency=margin_currency)
        elif initialMargining == InitialMargining.SIMM:
            self.im_model = SIMM(resultCurrency=margin_currency)
        elif initialMargining == InitialMargining.NO_IM:
            self.im_model = NOIMM(resultCurrency=margin_currency)

    def link_sa_ccr_instance(self, sa_ccr_instance):
        # Has to be done this way to avoid circular references between collateral agreement and SA_CCR
        if sa_ccr_instance.trades != []:
            raise (Exception('Should be an empty SA_CCR instance with no associated trades'))
        self.sa_ccr_model = sa_ccr_instance

    def add_trades(self, trades: Union[Trade, List[Trade]]):
        super().add_trades(trades=trades)
        self.im_model.add_trades(trades=trades)
        self.sa_ccr_model.add_trades(trades=trades)
        self.vm_model.add_trades(trades=trades)

    def remove_trades(self, trade_ids: Union[None, int, List[int]] = None,
                      trades: Union[None, Trade, List[Trade]] = None):
        super().remove_trades(trade_ids=trade_ids, trades=trades)
        self.im_model.remove_trades(trade_ids=trade_ids, trades=trades)
        self.sa_ccr_model.remove_trades(trade_ids=trade_ids, trades=trades)
        self.vm_model.remove_trades(trade_ids=trade_ids, trades=trades)

    def get_im_model(self):
        return self.im_model

    def get_sa_ccr_model(self):
        return self.sa_ccr_model

    def get_vm_model(self):
        return self.vm_model

    def get_C(self):
        return self.vm_model.get_vm() + self.get_nica()

    def get_nica(self):
        return self.im_model.get_im_receive() - self.unsegregated_overcollateraliziation_posted + self.segregated_overcollateralization_received + self.unsegregated_overcollateralization_received
