from enum import Enum


class TradeType(Enum):
    PUT = 'Put'
    CALL = 'Call'
    LINEAR = 'Linear'

class TradeDirection(Enum):
    SHORT = 'Short'  # A short trade looses value as the underlying rises in value - In a swap this is the Receiver side
    LONG = 'Long'  # A long trade rises in value as the underlying rises in value - In a swap this it the Payer side

class SwapDirection(Enum):
    RECEIVER = 'Fixed Rate Receiver Swap' #Corresponds to a short position as value increases as underlying rate falls
    PAYER = 'Fixed Rate Payer Swap' #Correpsonds to a long position as value increases as


class AssetClass(Enum):
    """
    Enum for the five asset classes defined in SA-CCR.
    """
    IR = 'Interest rate'
    EQ = 'Equity'
    CR = 'Credit'
    CO = 'Commodity'
    FX = 'Foreign exchange'


class MaturityBucket(Enum):
    ONE = 'Up to one year'
    TWO = 'One to five years'
    THREE = 'More than 5 years'


class SubClass(Enum):
    pass


class CreditSubClass(SubClass):
    AAA = 'AAA'
    AA = 'AA'
    A = 'A'
    BBB = 'BBB'
    BB = 'BB'
    B = 'B'
    CCC = 'CCC'

class EquitySubClass(SubClass):
    SINGLE_NAME = 'Single name'
    INDEX = 'Index'


class CommoditySubClass(SubClass):
    ELECTRICITY = 'Electricity'
    OIL_GAS = 'Oil/Gas'
    METALS = 'Metals'
    AGRICULTURAL = 'Agricultural'
    OTHER = 'Other'


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    CHF = 'CHF'
    JPY = 'JPY'

class Stock(Enum):
    ADS = 'Adidas'
    DBK = 'Deutsche Bank'

class CurrencyPair(Enum):
    EURUSD = 'EUR / USD'
    USDBRL = 'USD / BRL'
    USDCLP = 'USD / CLP'
    GBPUSD = 'GBP / USD'