from utilities.Enums import TradeDirection, TradeType
from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from instruments.interestRateInstrument.interestRateTrade import InterestRateTrade


class Swaption(InterestRateTrade):

    def __init__(self,
                 underlyingSwap: InterestRateSwap,
                 optionMaturity_in_days: float,
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
            t=optionMaturity_in_days/360,
            e=underlyingSwap.e,
            tradeType=tradeType,
            tradeDirection=tradeDirection
        )