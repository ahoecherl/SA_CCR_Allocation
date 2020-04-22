

class SA_CCR():

    def calculate_sa_ccr_ead(rc: float, pfe: float) -> float:
        """
        Calculate EAD of SA-CCR as defined in paragraph 186.

        :param rc: Replacement Cost
        :param pfe: Potential Future Exposure
        :return: Exposure at default according to SA-CCR
        """

        alpha = 1.4  # Carried over from alpha used for IMM
        return alpha * (rc + pfe)

    def multiplier(v: float, c: float, addOn_aggregate: float, floor: float = 0.05) -> float:
        """
        Multiplier calculation for SA-CCR

        :param v: Current value of the derivative transactions in the netting set
        :param c: Haircut value of the net collateral held
        :param addOn_aggregate: Aggregated (summed up) AddOn over all asset classes
        :param floor: Regulatory floor for the multiplier. Set to 5% in paragraph 149
        :return: Multiplier for PFE calculation according to SA-CCR
        """

        return min(1, floor + (1 - floor) * exp((v - c) / (2 * (1 - floor) * addOn_aggregate)))