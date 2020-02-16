from Enums import SwapDirection
from pricer.pricer import Pricer


class InterestRateSwapPricer(Pricer):
    pass

    def price(trade):
        if trade.swapDirection == SwapDirection.PAYER:
            return 30000
        elif trade.swapDirection == SwapDirection.RECEIVER:
            return -20000