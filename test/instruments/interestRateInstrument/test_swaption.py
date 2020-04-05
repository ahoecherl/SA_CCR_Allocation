from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from instruments.interestRateInstrument.swaption import Swaption
from utilities.Enums import Currency, SwapDirection, TradeDirection


def test_processSwaption():
    fw_swap = InterestRateSwap(notional=1000000, currency=Currency.USD, timeToSwapStart_in_days=1 * 360,
                               timeToSwapEnd_in_days=3 * 360, swapDirection=SwapDirection.PAYER)
    swaption = Swaption(underlyingSwap=fw_swap,
                        optionMaturity_in_days=1 * 360,
                        tradeDirection=TradeDirection.SHORT,
                        strikeFixedRate=0.014)
    print(swaption.get_price())
    print(swaption.get_delta())
