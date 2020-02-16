from utilities.Enums import TradeDirection, TradeType
from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade
from pricer.swaptionPricer import SwaptionPricer


class Swaption(InterestRateTrade):

    def __init__(self,
                 underlyingSwap: InterestRateSwap,
                 optionMaturity: float,
                 tradeDirection: TradeDirection,
                 strikeFixedRate: float,
                 forwardParFixedRate: float):
        if underlyingSwap.tradeDirection == TradeDirection.LONG:
            tradeType = TradeType.CALL  # A swaption on a payer Swap is a Call Swaption as the call's value raises as the interest rate rises
        else:
            tradeType = TradeType.PUT  # Vice versa the above
        self.S = forwardParFixedRate
        self.K = strikeFixedRate
        super(Swaption, self).__init__(
            notional=underlyingSwap.notional,
            currency=underlyingSwap.currency,
            s=underlyingSwap.s,
            m=underlyingSwap.e,  # assuming the Swaption is physically settled
            t=optionMaturity,
            e=underlyingSwap.e,
            tradeType=tradeType,
            tradeDirection=tradeDirection
        )

    def get_pricer(self):
        return SwaptionPricer