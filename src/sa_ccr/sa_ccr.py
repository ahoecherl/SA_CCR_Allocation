from math import exp, log, sqrt
from typing import List

from pandas import read_csv, Series
from scipy.stats import norm

from collateralAgreement import CollateralAgreement, Margining, Clearing, Tradecount, Dispute
from instruments.Trade import Trade
from utilities.Enums import AssetClass, TradeType, TradeDirection, SubClass, MaturityBucket


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

    def margining_factor(trade: Trade, ca: CollateralAgreement) -> float:
        if ca.margining == Margining.UNMARGINED:
            floored_maturity = max(10 / 250,
                                   trade.m)  # as Everything is measured in years 10/250 is equal to 10 business days.
            mf_unmargined = sqrt(min(floored_maturity, 1) / 1)
            return mf_unmargined
        if ca.margining == Margining.MARGINED:
            # Compare paragraph 164 to see how MPOR needs to be set for margined trades.
            if ca.clearing == Clearing.CLEARED:
                MPOR = 5
            elif ca.tradecount == Tradecount.OVER_FIVE_THOUSAND:
                MPOR = 20
            else:
                MPOR = 10
            if ca.dispute == Dispute.OUTSTANDING_DISPUTES:
                MPOR = MPOR * 2

            mf_margined = 3 / 2 * sqrt(
                MPOR / 250)  # Since MPOR above is defined in Business days and not year fractions division by 250 is necessary.
            return mf_margined

    def get_supervisory_factor(assetClass: AssetClass, subClass: SubClass = None) -> float:
        supervisory_parameter = read_csv('supervisory_parameters.csv')
        sf = None
        if subClass is None:
            sf = \
            supervisory_parameter[(supervisory_parameter.AssetClass == assetClass.value)]['Supervisory factor'].iloc[0]
        elif subClass is not None:
            sf = supervisory_parameter[(supervisory_parameter.AssetClass == assetClass.value) & (
                        supervisory_parameter.SubClass == subClass.value)]['Supervisory factor'].iloc[0]
        return sf

    def interest_rate_addOn(trades: List[Trade], ca: CollateralAgreement) -> float:
        bucketed_trades = {}
        en_cur_mat = {}
        add_on_cur = Series()
        currencies = set()

        for t in trades:
            key = (t.currency, t.get_maturity_bucket())
            currencies.add(t.currency)
            if key in bucketed_trades:
                bucketed_trades[key].append(t)
            else:
                bucketed_trades[key] = [t]

        for key, trades in bucketed_trades.items():
            effective_notional = 0
            for t in trades:
                effective_notional += SA_CCR.calculate_sa_ccr_delta(t) * SA_CCR.trade_level_adjusted_notional(t) * SA_CCR.margining_factor(t,
                                                                                                                      ca)
            en_cur_mat[key] = effective_notional

        for cur in currencies:
            d_1 = en_cur_mat.get((cur, MaturityBucket.ONE), 0)
            d_2 = en_cur_mat.get((cur, MaturityBucket.TWO), 0)
            d_3 = en_cur_mat.get((cur, MaturityBucket.THREE), 0)

            en_cur = sqrt(d_1 ** 2 + d_2 ** 2 + d_3 ** 2 + 1.4 * d_1 * d_2 + 1.4 * d_2 * d_3 + 0.6 * d_1 * d_3)

            add_on_cur[cur] = SA_CCR.get_supervisory_factor(assetClass=AssetClass.IR) * en_cur

        return add_on_cur.sum()