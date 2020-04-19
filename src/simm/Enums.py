from enum import Enum
import QuantLib as ql


class ProductClass(Enum):
    Equity = 'Equity'
    RatesFX = 'RatesFX'


class RiskType(Enum):
    Risk_IRCurve = 'Risk_IRCurve'
    Risk_Equity = 'Risk_Equity'
    Risk_IRVol = 'Risk_IRVol'
    Risk_EquityVol = 'Risk_EquityVol'
    Risk_FX = 'Risk_FX'

class ImRole(Enum):
    PLEDGOR = 'PLEDGOR'
    SECURED = 'SECURED'

SimmTenor = {ql.Period(2, ql.Weeks): '2w',
             ql.Period(1, ql.Months): '1m',
             ql.Period(3, ql.Months): '3m',
             ql.Period(6, ql.Months): '6m',
             ql.Period(1, ql.Years): '1y',
             ql.Period(2, ql.Years): '2y',
             ql.Period(3, ql.Years): '3y',
             ql.Period(5, ql.Years): '5y',
             ql.Period(10, ql.Years): '10y',
             ql.Period(15, ql.Years): '15y',
             ql.Period(20, ql.Years): '20y',
             ql.Period(30, ql.Years): '30y'}

class CrifColumn(Enum):
    TradeId = 'tradeId'
    ImModel = 'imModel'
    ProductClass = 'productClass'
    RiskType = 'riskType'
    Qualifier = 'qualifier'
    Bucket = 'bucket'
    Label1 = 'label1'
    Label2 = 'label2'
    Amount = 'amount'
    AmountCurrency = 'amountCurrency'
    AmountUSD = 'amountUSD'
    PostRegulation = 'postRegulation'
    CollectRegulation = 'collectRegulation'
    ValuationDate = 'valuationDate'
    EndDate = 'endDate'
    Notional = 'notional'
    NotionalCurrency = 'notionalCurrency'
    NotionalString = 'notionalString'

class EquityStaticData(Enum):
    ADS = {CrifColumn.Bucket: '5',
           CrifColumn.Qualifier: 'ISIN:DE000A1EWWW0'}
    DBK = {CrifColumn.Bucket: '7',
           CrifColumn.Qualifier: 'ISIN:DE0005140008'}