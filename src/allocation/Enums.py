from enum import Enum


class FdApproach(Enum):
    Absolute = 'Absolute bump'
    Relative = 'Relative bump'

class FdApproach2(Enum):
    Forward = 'Forward'
    Central = 'Central'
    Backward = 'Backward'