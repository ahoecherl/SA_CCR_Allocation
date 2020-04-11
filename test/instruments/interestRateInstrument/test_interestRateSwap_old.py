import QuantLib as ql
from pandas import DataFrame
from utilities.Enums import Currency, SwapDirection
from instruments.interestRateInstrument.interestRateSwap_old import InterestRateSwap
from marketdata import init_marketdata
from test.test_fixtures import *


def test_SwapPrice():
    notional = 10000000
    fixed_rate = 0.025
    float_spread = 0.004
    currency = Currency.USD
    ttstart = 5
    ttend = 10 * 360
    swap = InterestRateSwap(swapDirection=SwapDirection.PAYER, notional=notional, currency=currency,
                            timeToSwapStart_in_days=ttstart, timeToSwapEnd_in_days=ttend, fixed_rate=fixed_rate,
                            float_spread=float_spread)
    asdf = 1
    cashflows_fixed = DataFrame([(cf.date(), cf.amount()) for cf in swap.ql_swap.leg(0)], columns=["Date", "Amount"],
                                index=range(1, len(swap.ql_swap.leg(0)) + 1))
    cashflows_floating = DataFrame([(cf.date(), cf.amount()) for cf in swap.ql_swap.leg(1)], columns=["Date", "Amount"],
                                   index=range(1, len(swap.ql_swap.leg(1)) + 1))
    swap.ql_swap.leg(0)

    print(swap.get_price())
    asdf = 1




def test_Changing_Delta(standard_swap):
    from marketdata.interestRateCurves_old import flat_ois_quote
    flat_ois_quote.setValue(0.02)
    DV01_1 = standard_swap.get_delta()/10000
    flat_ois_quote.setValue(0.05)
    DV01_2 = standard_swap.get_delta()/10000
    asdf = 1