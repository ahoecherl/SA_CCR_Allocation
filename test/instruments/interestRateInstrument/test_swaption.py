from instruments.interestRateInstrument.irs import IRS
from instruments.interestRateInstrument.ois import OIS
from instruments.interestRateInstrument.swaption import Swaption
from marketdata.interestRateIndices import InterestRateIndex
from utilities.Enums import Currency, SwapDirection, TradeDirection
import pytest
from test.test_fixtures import *


def test_USDLIBOR3MSwaption(initialize_test):
    fw_swap = IRS(notional=1000000, timeToSwapStart=ql.Period(1, ql.Years), timeToSwapEnd=ql.Period(20, ql.Years),
                  swapDirection=SwapDirection.PAYER, index=InterestRateIndex.USDLIBOR3M)

    swaption = Swaption(underlyingSwap=fw_swap,
                        optionMaturity= ql.Period(1, ql.Years),
                        tradeDirection=TradeDirection.SHORT)
    print(swaption.get_price())
    print(swaption.get_delta())


def test_EURIBOR6MSwaption(initialize_test):
    fw_swap = IRS(notional=1000000, timeToSwapStart=ql.Period(1, ql.Years), timeToSwapEnd=ql.Period(20, ql.Years),
                  swapDirection=SwapDirection.PAYER, index=InterestRateIndex.EURIBOR6M)

    swaption = Swaption(underlyingSwap=fw_swap,
                        optionMaturity= ql.Period(1, ql.Years),
                        tradeDirection=TradeDirection.SHORT)
    print(swaption.get_price())
    print(swaption.get_delta())


def test_USD_irvol_sensi(initialize_test):
    tts = ql.Period(2, ql.Years)
    tte = ql.Period(10, ql.Years)
    swap1 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.USDLIBOR3M)
    swaption1 = Swaption(swap1, ql.Period(2, ql.Years))
    sensis1 = swaption1.get_simm_sensis_irvol()
    tts = ql.Period(6, ql.Months)
    swap2 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.USDLIBOR3M)
    swaption2 = Swaption(swap2, ql.Period(6, ql.Months))
    sensis2 = swaption2.get_simm_sensis_irvol()
    asdf =1


def test_EUR_irvol_sensi(initialize_test):
    tts = ql.Period(2, ql.Years)
    tte = ql.Period(10, ql.Years)
    swap1 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.EURIBOR6M)
    swaption1 = Swaption(swap1, ql.Period(2, ql.Years))
    sensis1 = swaption1.get_simm_sensis_irvol()
    tts = ql.Period(6, ql.Months)
    swap2 = IRS(600, tts, tte, SwapDirection.RECEIVER, InterestRateIndex.EURIBOR6M)
    swaption2 = Swaption(swap2, ql.Period(6, ql.Months))
    sensis2 = swaption2.get_simm_sensis_irvol()
    asdf = 1

