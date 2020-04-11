import QuantLib as ql

today = ql.Date(10, ql.May, 2019)

testVar2 = 5

day_count = ql.Actual360()

calendar = ql.UnitedStates()

business_day_convention = ql.ModifiedFollowing