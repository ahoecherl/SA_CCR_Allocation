import json
from enum import Enum
from typing import Union, List

from instruments.Trade import Trade
from margining.ccpimm import CCPIMM
from margining.noimm import NOIMM
from margining.simm import SIMM
from margining.variationMarginModel import NoVariationMargin, VariationMarginModel
from genericRiskMeasureModel import GenericRiskMeasureModel
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


class CollateralAgreement(GenericRiskMeasureModel):

    def __init__(self,
                 margining: Margining = Margining.MARGINED,
                 clearing: Clearing = Clearing.UNCLEARED,
                 initialMargining: InitialMargining = InitialMargining.SIMM,
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

        self.sync_vm_model = True
        self.sync_im_model = True
        self.sync_sa_ccr_model = True

    def link_sa_ccr_instance(self, sa_ccr_instance):
        # Has to be done this way to avoid circular references between collateral agreement and SA_CCR
        if sa_ccr_instance.trades != []:
            raise (Exception('Should be an empty SA_CCR instance with no associated trades'))
        self.sa_ccr_model = sa_ccr_instance

    def add_trades(self, trades: Union[Trade, List[Trade]]):
        super().add_trades(trades=trades)
        if self.sync_im_model:
            self.im_model.add_trades(trades=trades)
        if self.sync_sa_ccr_model:
            self.sa_ccr_model.add_trades(trades=trades)
        if self.sync_vm_model:
            self.vm_model.add_trades(trades=trades)

    def remove_trades(self,
                      trades: Union[None, Trade, List[Trade]] = None):
        super().remove_trades(trades=trades)
        if self.sync_im_model:
            self.im_model.remove_trades(trades=trades)
        if self.sync_sa_ccr_model:
            self.sa_ccr_model.remove_trades(trades=trades)
        if self.sync_vm_model:
            self.vm_model.remove_trades(trades=trades)

    def remove_all_trades(self):
        super().remove_all_trades()
        if self.sync_im_model:
            self.im_model.remove_all_trades()
        if self.sync_sa_ccr_model:
            self.sa_ccr_model.remove_all_trades()
        if self.sync_vm_model:
            self.vm_model.remove_all_trades()

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

    @property
    def sync_im_model(self):
        return self.__sync_im_model

    @property
    def sync_vm_model(self):
        return self.__sync_vm_model

    @property
    def sync_sa_ccr_model(self):
        return self.__sync_sa_ccr_model

    @sync_im_model.setter
    def sync_im_model(self, value : bool):
        try:
            if value == True and self.__sync_im_model == False:
                self.im_model.remove_all_trades()
                self.im_model.add_trades(self.trades)
        except AttributeError:
            pass
        self.__sync_im_model = value

    @sync_vm_model.setter
    def sync_vm_model(self, value: bool):
        try:
            if value == True and self.__sync_vm_model == False:
                self.vm_model.remove_all_trades()
                self.vm_model.add_trades(self.trades)
        except AttributeError:
            pass
        self.__sync_vm_model = value

    @sync_sa_ccr_model.setter
    def sync_sa_ccr_model(self, value: bool):
        try:
            if value == True and self.__sync_sa_ccr_model == False:
                self.sa_ccr_model.remove_all_trades()
                self.sa_ccr_model.add_trades(self.trades)
        except AttributeError:
            pass
        self.__sync_sa_ccr_model = value