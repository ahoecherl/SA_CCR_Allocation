from enum import Enum

from marketdata.marketData import marketData


class FxSpot(Enum, marketData):
    USDGBP = 0.9
    USDEUR = 0.8