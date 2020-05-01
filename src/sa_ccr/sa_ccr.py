from math import exp, log, sqrt

from pandas import read_csv
from scipy.stats import norm

from instruments.Trade import Trade
from utilities.Enums import AssetClass, TradeType, TradeDirection


class SA_CCR():

    def calculate_sa_ccr_ead(rc: float, pfe: float) -> float:
        """
        Calculate EAD of SA-CCR as defined in paragraph 186.
        Class function.

        :param rc: Replacement Cost
        :param pfe: Potential Future Exposure
        :return: Exposure at default according to SA-CCR
        """

        alpha = 1.4  # Carried over from alpha used for IMM
        return alpha * (rc + pfe)

    def multiplier(V: float, C: float, addOn_aggregate: float, floor: float = 0.05) -> float:
        """
        Multiplier calculation for SA-CCR

        :param V: Current value of the derivative transactions in the netting set
        :param C: Haircut value of the net collateral held
        :param addOn_aggregate: Aggregated (summed up) AddOn over all asset classes
        :param floor: Regulatory floor for the multiplier. Set to 5% in paragraph 149
        :return: Multiplier for PFE calculation according to SA-CCR
        """


        return min(1, floor + (1 - floor) * exp((V - C) / (2 * (1 - floor) * addOn_aggregate)))

    def trade_level_adjusted_notional(trade: Trade):
        """
        Calculates the trade level adjusted notional as defined in paragraph 157

        :param trade: Trade object for which the adjusted notional should be calculated
        :param underlying_price:
            required for FX trades (exchange rate to domestic currency)
            required for EQ trades (current price of one share)
            required for CO trades (current price of fone unit of commodity)
            not required for IR trades and CR trades

        :return: adjusted notional as defined in paragraph 157
        """

        if trade.assetClass in (AssetClass.IR, AssetClass.CR):
            sd = (exp(-0.05 * trade.s) - exp(-0.05 * trade.e)) / 0.05
            return trade.notional * sd

        # This assumes that trade.Notional is defined as quantity of underlying shares for equity and foreign currency notional for FX
        if trade.assetClass == AssetClass.EQ:
            return trade.notional * trade.S

        if trade.assetClass == AssetClass.FX:
            return trade.notional

    def get_supervisory_volatility(trade: Trade) -> float:
        supervisory_parameter = read_csv('supervisory_parameters.csv')
        sigma = None
        if trade.subClass is None:
            sigma = supervisory_parameter[(supervisory_parameter.AssetClass == trade.assetClass.value)][
                'SupervisoryOptionVolatility'].iloc[0]
        elif trade.subClass is not None:
            sigma = supervisory_parameter[(supervisory_parameter.AssetClass == trade.assetClass.value) & (
                        supervisory_parameter.SubClass == trade.subClass.value)]['SupervisoryOptionVolatility'].iloc[0]
        return sigma

    def calculate_sa_ccr_delta(trade) -> float:
        if (trade.tradeType == TradeType.LINEAR) and (trade.tradeDirection == TradeDirection.LONG):
            return 1
        elif (trade.tradeType == TradeType.LINEAR) and (trade.tradeDirection == TradeDirection.SHORT):
            return -1
        elif trade.tradeType in (TradeType.CALL, TradeType.PUT):
            d1_mult = +1 if trade.tradeType == TradeType.CALL else -1

            if trade.tradeType == TradeType.CALL and trade.tradeDirection == TradeDirection.LONG:
                n_mult = 1
            elif trade.tradeType == TradeType.CALL and trade.tradeDirection == TradeDirection.SHORT:
                n_mult = -1
            elif trade.tradeType == TradeType.PUT and trade.tradeDirection == TradeDirection.LONG:
                n_mult = -1
            else:
                n_mult = +1

            sigma = SA_CCR.get_supervisory_volatility(trade)

            d1 = (log(trade.S / trade.K) + 0.5 * sigma ** 2 * trade.t) / (sigma * sqrt(trade.t))

            delta = n_mult * norm.cdf(d1_mult * d1)
            return delta