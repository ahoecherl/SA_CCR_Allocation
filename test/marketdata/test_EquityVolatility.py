from marketdata.EquityVolatility import EquityVolatility, EquityVolatilityQuotes
import QuantLib as ql


def test_equity_volatilty():
    EquityVolatility.ADS

EquityVolatility.ADS.value.linkTo(
    EquityVolatilityQuotes.ADS.value.get_atm_shifted_surface_abs_one_pct(ql.Period(2, ql.Years)))
def test_shift_equity_volatility():
    pass