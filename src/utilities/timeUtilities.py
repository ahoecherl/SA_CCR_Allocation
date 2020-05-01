import QuantLib as ql

def convert_period_to_days(period:ql.Period) -> ql.Period:
    if period.units()==ql.Days:
        return period.length()
    if period.units()==ql.Weeks:
        return period.length()*7
    elif period.units() == ql.Months:
        return period.length()*30
    elif period.units() == ql.Years:
        return period.length()*360