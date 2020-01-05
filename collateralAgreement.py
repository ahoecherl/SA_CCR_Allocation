import json
from enum import Enum


class Margining(Enum):
    MARGINED = 'Margined'
    UNMARGINED = 'Unmargined'

class Tradecount(Enum):
    UNDER_FIVE_THOUSAND = 'Under five thousand transactions between the counterparties'
    OVER_FIVE_THOUSAND = 'Five thousand or more transactions between the counterparties (sadly not 9000)'

class Clearing(Enum):
    UNCLEARED = 'Non-centrally cleared derivatives'
    CLEARED = 'Centrally cleared derivatives'

class Dispute(Enum):
    NO_OUTSTANDING_DISPUTES = 'No margining disputes are outstanding between the counterparties'
    OUTSTANDING_DISPUTES = 'Disputes are outstanding between the counterparties'

class CollateralAgreement():

    def __init__(self,
                 margining : Margining = Margining.UNMARGINED,
                 clearing: Clearing = Clearing.UNCLEARED,
                 tradecount: Tradecount = Tradecount.UNDER_FIVE_THOUSAND,
                 dispute: Dispute = Dispute.NO_OUTSTANDING_DISPUTES,
                 threshold: float = 0.0,
                 mta: float = 0.0,
                 vm: float = 0.0,
                 posted_im: float = 0.0,
                 received_im: float = 0.0,
                 unsegregated_overcollateraliziation_posted: float = 0.0,
                 unsegregated_overcollateralization_received: float = 0.0,
                 segregated_overcollateralization_posted: float = 0.0,
                 segregated_overcollateralization_received: float = 0.0):
        self.margining = margining
        self.clearing = clearing
        self.tradecount = tradecount
        self.dispute = dispute
        self.threshold = threshold
        self.mta = mta
        self.vm = vm
        self.posted_im = posted_im
        self.received_im = received_im
        self.unsegregated_overcollateraliziation_posted = unsegregated_overcollateraliziation_posted
        self.unsegregated_overcollateralization_received = unsegregated_overcollateralization_received
        self.segregated_overcollateralization_posted = segregated_overcollateralization_posted
        self.segregated_overcollateralization_received = segregated_overcollateralization_received

    def __str__(self):
        return json.dumps({'margining': self.margining.value,
                           'clearing': self.clearing.value,
                           'tradecount': self.tradecount.value,
                           'dispute': self.dispute.value,
                           'threshold': self.threshold,
                           'mta': self.mta,
                           'vm': self.vm,
                           'posted_im': self.posted_im,
                           'received_im': self.received_im,
                           'unsegregated_overcollateraliziation_posted': self.unsegregated_overcollateraliziation_posted,
                           'unsegregated_overcollateralization_received': self.unsegregated_overcollateralization_received,
                           'segregated_overcollateralization_posted': self.segregated_overcollateralization_posted,
                           'segregated_overcollateralization_received': self.segregated_overcollateralization_received},
                          indent=4)