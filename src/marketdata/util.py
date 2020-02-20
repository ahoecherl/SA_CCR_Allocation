import QuantLib as ql

today = ql.Date(10, ql.May, 2019)

testVar2 = 5

calendar = ql.UnitedStates()

day_count = ql.Actual360()

business_day_convention = ql.ModifiedFollowing