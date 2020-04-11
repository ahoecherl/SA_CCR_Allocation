from enum import Enum
import QuantLib as ql

from utilities.Enums import Currency


class InterestRateSwapConventions(Enum):
    EURIBOR6M = {'FixedFrequency': ql.Annual,
                 'FloatFrequency': ql.Semiannual,
                 'Currency': Currency.EUR,
                 'DateRoll': ql.ModifiedFollowing,
                 'Calendar': ql.TARGET(),
                 'FixedDayCount': ql.Thirty360(),
                 'FloatDayCount': ql.Actual360(),
                 'SettlementLag': 2}

    USDLIBOR3M = {'FixedFrequency': ql.Semiannual,
                  'FloatingFrequency': ql.Quarterly,
                  'Currency': Currency.USD,
                  'DateRoll': ql.ModifiedFollowing,
                  'Calendar': ql.UnitedStates(ql.UnitedStates.NYSE),
                  'FixedDayCount': ql.Thirty360(),
                  'FloatDayCount': ql.Actual360(),
                  'SettlementLag': 2}


class OvernightIndexedSwapConventions(Enum):
    EONIA = {'FixedFrequency': ql.Annual,
             'FloatFrequency': ql.Annual,
             'Calendar': ql.TARGET(),
             'Currency': Currency.EUR,
             'DayCount': ql.Actual360(),
             'DateRoll': ql.ModifiedFollowing,
             'SettlementLag': 2
             }

    FEDFUNDS = {'FixedFrequency': ql.Annual,
                'FloatFrequency': ql.Annual,
                'Calendar': ql.UnitedStates(ql.UnitedStates.NYSE),
                'Currency': Currency.USD,
                'DayCount': ql.Actual360(),
                'DateRoll': ql.ModifiedFollowing,
                'SettlementLag': 2}


class ForwardRateAgreementConventions(Enum):
    USDLIBOR3M = {'SettlementLag': 2,
                  'Tenor': ql.Period(3, ql.Months),
                  'DayCount': ql.ModifiedFollowing,
                  'Calendar': ql.UnitedStates.NYSE}

