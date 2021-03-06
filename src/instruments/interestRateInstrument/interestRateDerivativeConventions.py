from enum import Enum
import QuantLib as ql

from utilities.Enums import Currency


class IRSConventions(Enum):
    EURIBOR6M = {'FixedFrequency': ql.Annual,
                 'FloatFrequency': ql.Semiannual,
                 'Currency': Currency.EUR,
                 'DateRoll': ql.ModifiedFollowing,
                 'Calendar': ql.TARGET(),
                 'FixedDayCount': ql.Thirty360(),
                 'FloatDayCount': ql.Actual360(),
                 'DateGeneration': ql.DateGeneration.Forward,
                 'EndOfMonth': False,
                 'SettlementLag': 2}

    USDLIBOR3M = {'FixedFrequency': ql.Semiannual,
                  'FloatFrequency': ql.Quarterly,
                  'Currency': Currency.USD,
                  'DateRoll': ql.ModifiedFollowing,
                  'Calendar': ql.UnitedStates(ql.UnitedStates.NYSE),
                  'FixedDayCount': ql.Thirty360(),
                  'FloatDayCount': ql.Actual360(),
                  'DateGeneration': ql.DateGeneration.Forward,
                  'EndOfMonth': False,
                  'SettlementLag': 2}


class OISConventions(Enum):
    EONIA = {'FixedFrequency': ql.Annual,
             'FloatFrequency': ql.Annual,
             'Calendar': ql.TARGET(),
             'Currency': Currency.EUR,
             'DayCount': ql.Actual360(),
             'DateRoll': ql.ModifiedFollowing,
             'DateGeneration': ql.DateGeneration.Forward,
             'EndOfMonth': False,
             'SettlementLag': 2
             }

    FEDFUNDS = {'FixedFrequency': ql.Annual,
                'FloatFrequency': ql.Annual,
                'Calendar': ql.UnitedStates(ql.UnitedStates.NYSE),
                'Currency': Currency.USD,
                'DayCount': ql.Actual360(),
                'DateRoll': ql.ModifiedFollowing,
                'DateGeneration': ql.DateGeneration.Forward,
                'EndOfMonth': False,
                'SettlementLag': 2}


class FRAConventions(Enum):
    USDLIBOR3M = {'SettlementLag': 2,
                  'Tenor': ql.Period(3, ql.Months),
                  'DayCount': ql.ModifiedFollowing,
                  'Calendar': ql.UnitedStates.NYSE}


class SwaptionConventions(Enum):
    EUR = {'Calendar': IRSConventions.EURIBOR6M.value['Calendar'],
           'DateRoll': IRSConventions.EURIBOR6M.value['DateRoll'],
           'DayCount': IRSConventions.EURIBOR6M.value['FloatDayCount'],
           'Pricer': ql.BachelierSwaptionEngine}

    USD = {'Calendar': IRSConventions.USDLIBOR3M.value['Calendar'],
           'DateRoll': IRSConventions.USDLIBOR3M.value['DateRoll'],
           'DayCount': IRSConventions.USDLIBOR3M.value['FloatDayCount'],
           'Pricer': ql.BlackSwaptionEngine}
