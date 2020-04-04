import QuantLib as ql
from pandas import DataFrame
from utilities.Enums import Currency, SwapDirection
from instruments.interestRateInstrument.interestRateSwap import InterestRateSwap
from marketdata import init_marketdata


def test_SwapPrice():
    notional = 10000000
    fixed_rate = 0.025
    float_spread = 0.004
    currency = Currency.USD
    ttstart = 5/365
    ttend = 10
    swap = InterestRateSwap(swapDirection=SwapDirection.PAYER, notional=notional, currency=currency, timeToSwapStart_in_days= ttstart, timeToSwapEnd_in_days= ttend, fixed_rate = fixed_rate, float_spread = float_spread)
    asdf = 1
    cashflows_fixed = DataFrame([(cf.date(), cf.amount()) for cf in swap.ql_swap.leg(0)], columns = ["Date", "Amount"], index = range(1, len(swap.ql_swap.leg(0))+1))
    cashflows_floating = DataFrame([(cf.date(), cf.amount()) for cf in swap.ql_swap.leg(1)], columns=["Date", "Amount"],
                                index=range(1, len(swap.ql_swap.leg(1)) + 1))
    swap.ql_swap.leg(0)

    print(swap.get_price())
    asdf = 1