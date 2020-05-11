from architecture_blueprint.riskMeasureModel import RiskMeasureModel


class InitialMarginModel(RiskMeasureModel):

    def __init__(self, marginCurrency):
        super().__init__()
        self.marginCurrency = marginCurrency

    def calculate_risk_measure(self):
        # Calculates initial margin to be posted and received, if necessary converts it to the correct margin currency
        # The margin currency is usually defined in the collateral agreement to which this margin model belongs
        return {'im_receive': self.calculate_im_receive(),
                'im_post': self.calculate_im_post()}

    def calculate_im_receive(self):
        pass

    def calculate_im_post(self):
        pass


class NoIMM(InitialMarginModel):
    # This model is used as IM Model if no initial margining is in place for the collateral agreement
    def __init__(self):
        super().__init__(Currency.USD)
        pass

    def calculate_im_receive(self):
        return 0

    def calculate_im_post(self):
        return 0


class SIMM(InitialMarginModel):
    # This model is used as IM Model if the associated collateral agreement dictates, that the portfolio is bilateral
    # and that initial margin is exchanged and should be calculated using SIMM.
    def __init__(self, marginCurrency, calculationCurrency):
        super().__init__(marginCurrency)
        self.suplementary_crif_entries = None
        self.calculationCurrency = calculationCurrency

    def set_suplementary_crif_entries(self, input):
        # Sets optional additional crif entries such as AddOns. These can e.g. be mandated to use by the regulator
        # or to counteract poor backtesting performance of specific portfolio. They are used seldom and if used they
        # should be quite static.
        self.suplementary_crif_entries = input

    def simm_calculation(self, role):
        # Gather all crif entries and call an external SIMM aggregator function that calculates an IM value given a
        # CRIF, role and calculation currency. If the role is 'post' all input sensitivities are multiplied by -1
        crif = [t.get_simm_sensitivities() for t in self.portfolio.trades]
        crif += self.suplementary_crif_entries
        SIMM.simm_aggregator(crif, role, self.calculationCurrency)

    def calculate_im_receive(self):
        return self.simm_calculation(role='receive')

    def calculate_im_post(self):
        return self.simm_calculation(role='post')

    @staticmethod
    def simm_aggregator(crif, role, calculationCurrency) -> float:
        # This can be a static class function not specific to a single instance of the SIMM class. It could also be placed
        # outside of the class and e.g. accessed via an API. Calculates the IM quoted in USD
        pass


class CCPIMM(InitialMarginModel):
    # This model is used as IM Model if the associated collateral agreement relates to a portfolio that is cleared
    # through a CCP

    def calculate_im_receive(self):
        # a CCP generally does not post IM to the bank
        return 0

    def calculate_im_post(self):
        # some approximation of an internal initial margin model of a CCP. Is based on the current portfolio accessible
        # through self.portfolio.trades. Therefore also changes if trade notional get bumped e.g. for Euler Allocation
        pass


class ScheduleIMM(InitialMarginModel):
    # This model is used as IM Model if the associated collateral agreement relates to a portfolio for which IM is
    # calculated using the standardized or schedule IM approach. In contrast, SIMM is classified as an internal model.
    # It can be necessary to run the two models in parallel if some counterparties are unable to handle SIMM. The model
    # is based on trade notionals and therefore also changes in value as the the portfolio at self.portfolio.trades
    # changes or if the notional of trades in it are bumped.

    def __init__(self, marginCurrency, calculationCurrency):
        super().__init__(marginCurrency)
        self.suplementary_crif_entries = None
        self.calculationCurrency = calculationCurrency

    def schedule_calculation(self, role):
        crif = [t.get_schedule_crif_entries() for t in self.portfolio.trades]
        crif += self.suplementary_crif_entries
        SIMM.simm_aggregator(crif, role, self.calculationCurrency)

    def calculate_im_receive(self):
        return self.schedule_calculation(role='receive')

    def calculate_im_post(self):
        return self.schedule_calculation(role='post')

    def set_suplementary_crif_entries(self, input):
        self.suplementary_crif_entries = input

    @staticmethod
    def schedule_aggregator(crif, role, calculationCurrency) -> float:
        pass
