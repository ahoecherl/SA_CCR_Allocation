from enum import Enum

import QuantLib as ql

from instruments.interestRateInstrument.interestRateDerivativeConventions import OvernightIndexedSwapConventions, \
    InterestRateSwapConventions, ForwardRateAgreementConventions


class InterestRateCurveQuotes(Enum):
    EONIA = {ql.Period(2, ql.Weeks): ql.SimpleQuote(-0.36503 / 100),
             ql.Period(1, ql.Months): ql.SimpleQuote(-0.3650 / 100),
             ql.Period(3, ql.Months): ql.SimpleQuote(-0.36521 / 100),
             ql.Period(6, ql.Months): ql.SimpleQuote(-0.36754 / 100),
             ql.Period(1, ql.Years): ql.SimpleQuote(-0.37488 / 100),
             ql.Period(2, ql.Years): ql.SimpleQuote(-0.36102 / 100),
             ql.Period(3, ql.Years): ql.SimpleQuote(-0.31511 / 100),
             ql.Period(5, ql.Years): ql.SimpleQuote(-0.17438 / 100),
             ql.Period(10, ql.Years): ql.SimpleQuote(0.28879 / 100),
             ql.Period(15, ql.Years): ql.SimpleQuote(0.62908 / 100),
             ql.Period(20, ql.Years): ql.SimpleQuote(0.82255 / 100),
             ql.Period(30, ql.Years): ql.SimpleQuote(0.92238 / 100)}

    EURIBOR6M = {ql.Period(6, ql.Months): ql.SimpleQuote(-0.231 / 100),
                 ql.Period(1, ql.Years): ql.SimpleQuote(-0.2355 / 100),
                 ql.Period(2, ql.Years): ql.SimpleQuote(-0.20860 / 100),
                 ql.Period(3, ql.Years): ql.SimpleQuote(-0.1525 / 100),
                 ql.Period(5, ql.Years): ql.SimpleQuote(-0.17438 / 100),
                 ql.Period(10, ql.Years): ql.SimpleQuote(0.28879 / 100),
                 ql.Period(15, ql.Years): ql.SimpleQuote(0.62908 / 100),
                 ql.Period(20, ql.Years): ql.SimpleQuote(0.82255 / 100),
                 ql.Period(30, ql.Years): ql.SimpleQuote(0.92238 / 100)}

    FEDFUNDS = {ql.Period(2, ql.Weeks): ql.SimpleQuote(2.372 / 100),
                ql.Period(1, ql.Months): ql.SimpleQuote(2.375 / 100),
                ql.Period(3, ql.Months): ql.SimpleQuote(2.364 / 100),
                ql.Period(6, ql.Months): ql.SimpleQuote(2.335 / 100),
                ql.Period(1, ql.Years): ql.SimpleQuote(2.248 / 100),
                ql.Period(2, ql.Years): ql.SimpleQuote(2.087 / 100),
                ql.Period(3, ql.Years): ql.SimpleQuote(2.019 / 100),
                ql.Period(5, ql.Years): ql.SimpleQuote(2.015 / 100),
                ql.Period(10, ql.Years): ql.SimpleQuote(2.168 / 100),
                ql.Period(15, ql.Years): ql.SimpleQuote(2.277 / 100),
                ql.Period(20, ql.Years): ql.SimpleQuote(2.323 / 100),
                ql.Period(30, ql.Years): ql.SimpleQuote(2.337 / 100)}

    USDLIBOR3M = {ql.Period(3, ql.Months): ql.SimpleQuote(2.52788 / 100),
                  ql.Period(6, ql.Months): ql.SimpleQuote(2.463 / 100),
                  ql.Period(1, ql.Years): ql.SimpleQuote(2.453 / 100),
                  ql.Period(2, ql.Years): ql.SimpleQuote(2.2301 / 100),
                  ql.Period(3, ql.Years): ql.SimpleQuote(2.26 / 100),
                  ql.Period(5, ql.Years): ql.SimpleQuote(2.257 / 100),
                  ql.Period(10, ql.Years): ql.SimpleQuote(2.41 / 100),
                  ql.Period(15, ql.Years): ql.SimpleQuote(2.523 / 100),
                  ql.Period(20, ql.Years): ql.SimpleQuote(2.574 / 100),
                  ql.Period(30, ql.Years): ql.SimpleQuote(2.593 / 100)}


def __create_eonia_curve_handle__():
    # all quotes are OIS quotes
    eonia_index = ql.Eonia()
    eonia_ois_conventions = OvernightIndexedSwapConventions.EONIA.value
    eonia_helpers = []
    for tenor, quote in InterestRateCurveQuotes.EONIA.value.items():
        eonia_helpers.append(ql.OISRateHelper(eonia_ois_conventions['SettlementLag'],
                                              tenor,
                                              ql.QuoteHandle(quote),
                                              eonia_index))

    eonia_curve = ql.PiecewiseLogCubicDiscount(eonia_ois_conventions['SettlementLag'],
                                               eonia_ois_conventions['Calendar'],
                                               eonia_helpers,
                                               eonia_ois_conventions['DayCount'])
    eonia_curve.enableExtrapolation()
    return ql.YieldTermStructureHandle(eonia_curve)


def __create_fedfunds_curve_handle__():
    # all quotes are OIS quotes
    fedfunds_index = ql.FedFunds()
    fedfunds_ois_conventions = OvernightIndexedSwapConventions.FEDFUNDS.value
    fedfunds_helpers = []
    for tenor, quote in InterestRateCurveQuotes.FEDFUNDS.value.items():
        fedfunds_helpers.append(ql.OISRateHelper(fedfunds_ois_conventions['SettlementLag'],
                                                 tenor,
                                                 ql.QuoteHandle(quote),
                                                 fedfunds_index))

    fedfunds_curve = ql.PiecewiseLogCubicDiscount(fedfunds_ois_conventions['SettlementLag'],
                                                  fedfunds_ois_conventions['Calendar'],
                                                  fedfunds_helpers,
                                                  fedfunds_ois_conventions['DayCount'])
    fedfunds_curve.enableExtrapolation()
    return ql.YieldTermStructureHandle(fedfunds_curve)


class OisCurve(Enum):
    EONIA = __create_eonia_curve_handle__()
    FEDFUNDS = __create_fedfunds_curve_handle__()


def __create_euribor6m_curve_handle__():
    # here we hardcode that the first quote is a money market quote and all other quotes are swap quotes
    # We are using the EONIA curve as discount curve in bootstrapping
    # We are using the conventions for Euribor6m swap for the deposit as well, which is fine in this case

    euribor6m_swap_conventions = InterestRateSwapConventions.EURIBOR6M.value
    fixing_key = ql.Period(6, ql.Months)
    money_market_quotes = {k: InterestRateCurveQuotes.EURIBOR6M.value[k] for k in [fixing_key]}
    swap_quotes = dict(InterestRateCurveQuotes.EURIBOR6M.value)
    del swap_quotes[fixing_key]

    euribor6m_helpers = []
    for tenor, quote in money_market_quotes.items():
        euribor6m_helpers.append(ql.DepositRateHelper(ql.QuoteHandle(quote),
                                                      tenor,
                                                      euribor6m_swap_conventions['SettlementLag'],
                                                      euribor6m_swap_conventions['Calendar'],
                                                      euribor6m_swap_conventions['DateRoll'],
                                                      euribor6m_swap_conventions['EndOfMonth'],
                                                      euribor6m_swap_conventions['FloatDayCount']))

    discountcurve = OisCurve.EONIA.value

    for tenor, quote in swap_quotes.items():
        euribor6m_helpers.append(ql.SwapRateHelper(ql.QuoteHandle(quote),
                                                   tenor,
                                                   euribor6m_swap_conventions['Calendar'],
                                                   euribor6m_swap_conventions['FixedFrequency'],
                                                   euribor6m_swap_conventions['DateRoll'],
                                                   euribor6m_swap_conventions['FixedDayCount'],
                                                   ql.Euribor6M(),
                                                   ql.QuoteHandle(),  # no Spread
                                                   ql.Period(0, ql.Days),  # no Spread
                                                   discountcurve))

    euribor6m_curve = ql.PiecewiseLogCubicDiscount(euribor6m_swap_conventions['SettlementLag'],
                                                   euribor6m_swap_conventions['Calendar'],
                                                   euribor6m_helpers,
                                                   euribor6m_swap_conventions['FloatDayCount'])
    euribor6m_curve.enableExtrapolation()

    return ql.YieldTermStructureHandle(euribor6m_curve)


def __create_usdlibor3m_curve_handle__():
    # here we hardcode that the 3M quote is a money market quote and the 6M quote is a FRA. All other quotes are Swaps
    # We are using the conventions of the Swap for the desposit which is fine since they are the same.

    usdlibor3m_swap_conventions = InterestRateSwapConventions.USDLIBOR3M.value
    index = ql.USDLibor(ql.Period(3, ql.Months))

    fixing_keys = [ql.Period(3, ql.Months)]
    fra_keys = [ql.Period(6, ql.Months)]
    money_market_quotes = {k: InterestRateCurveQuotes.USDLIBOR3M.value[k] for k in fixing_keys}
    fra_quotes = {k: InterestRateCurveQuotes.USDLIBOR3M.value[k] for k in fra_keys}

    swap_quotes = dict(InterestRateCurveQuotes.USDLIBOR3M.value)
    # keys =
    for key in fixing_keys + fra_keys:
        del swap_quotes[key]

    usdlibor3m_helpers = []
    for tenor, quote in money_market_quotes.items():
        usdlibor3m_helpers.append(ql.DepositRateHelper(ql.QuoteHandle(quote),
                                                       tenor,
                                                       usdlibor3m_swap_conventions['SettlementLag'],
                                                       usdlibor3m_swap_conventions['Calendar'],
                                                       usdlibor3m_swap_conventions['DateRoll'],
                                                       usdlibor3m_swap_conventions['EndOfMonth'],
                                                       usdlibor3m_swap_conventions['FloatDayCount']))

    usdlibor3m_fra_conventions = ForwardRateAgreementConventions.USDLIBOR3M.value
    for tenor, quote in fra_quotes.items():
        usdlibor3m_helpers.append(ql.FraRateHelper(ql.QuoteHandle(quote),
                                                   tenor.length() - usdlibor3m_fra_conventions['Tenor'].length(),
                                                   # yields the start date of the FRA
                                                   index
                                                   ))

    discountcurve = OisCurve.FEDFUNDS.value
    for tenor, quote in swap_quotes.items():
        usdlibor3m_helpers.append(ql.SwapRateHelper(ql.QuoteHandle(quote),
                                                    tenor,
                                                    usdlibor3m_swap_conventions['Calendar'],
                                                    usdlibor3m_swap_conventions['FixedFrequency'],
                                                    usdlibor3m_swap_conventions['DateRoll'],
                                                    usdlibor3m_swap_conventions['FixedDayCount'],
                                                    index,
                                                    ql.QuoteHandle(),  # no Spread
                                                    ql.Period(0, ql.Days),  # no Spread
                                                    discountcurve))

    usdlibor3m_curve = ql.PiecewiseLogCubicDiscount(usdlibor3m_swap_conventions['SettlementLag'],
                                                    usdlibor3m_swap_conventions['Calendar'],
                                                    usdlibor3m_helpers,
                                                    usdlibor3m_swap_conventions['FloatDayCount'])
    usdlibor3m_curve.enableExtrapolation()

    return ql.YieldTermStructureHandle(usdlibor3m_curve)


class LiborCurve(Enum):
    EURIBOR6M = __create_euribor6m_curve_handle__()
    USDLIBOR3M = __create_usdlibor3m_curve_handle__()
