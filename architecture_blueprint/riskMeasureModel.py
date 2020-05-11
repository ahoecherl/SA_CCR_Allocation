class RiskMeasureModel:

    def __init__(self):
        self.portfolio = None

    def get_risk_measure(self):
        # Lazy method that only recalculates the risk measure with calculate_risk_measure() if the portfolio it is
        # referencing is changed or if the used marketdata has changed over the course of time
        pass

    def calculate_risk_measure(self):
        pass