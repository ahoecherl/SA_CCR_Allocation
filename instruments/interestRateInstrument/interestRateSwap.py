from Enums import Currency, TradeDirection, TradeType, SwapDirection
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade
from pricer.interestRateSwapPricer import InterestRateSwapPricer


class InterestRateSwap(InterestRateTrade):

    def __init__(self,
                 notional: float,
                 currency: Currency,
                 timeToSwapStart: float,
                 timeToSwapEnd: float,
                 swapDirection: SwapDirection  # Payer is Long, Receiver is Short the underlying
                 ):
        self.swapDirection = swapDirection
        if swapDirection == SwapDirection.PAYER: tradeDirection = TradeDirection.LONG
        if swapDirection == SwapDirection.RECEIVER: tradeDirection = TradeDirection.SHORT
        super(InterestRateSwap, self).__init__(
            notional=notional,
            currency=currency,
            s=timeToSwapStart,
            m=timeToSwapEnd,
            e=timeToSwapEnd,
            t=None,
            tradeDirection=tradeDirection,
            tradeType=TradeType.LINEAR
        )

    def get_pricer(self):
        return InterestRateSwapPricer