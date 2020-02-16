import QuantLib as ql

today = ql.Date(20, ql.October, 2015)

calendar = ql.UnitedStates()

day_count = ql.Actual365Fixed()

business_day_convention = ql.ModifiedFollowing