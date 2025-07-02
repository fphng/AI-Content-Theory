import numpy as np
from scipy.optimize import brentq

class Creator:
    """
    Represents a single creator agent who optimizes their content strategy.
    """

    def __init__(self, talent_theta: float, params: dict):
        if not 0 <= talent_theta <= 1:
            raise ValueError("Talent theta must be between 0 and 1.")
        
        self.talent_theta = talent_theta
        self.params = params

    def _get_value(self, delta: float) -> float:
        return self.params['beta_0'] + self.params['beta_1'] * self.talent_theta + self.params['beta_2'] * delta

    def _get_novelty_multiplier(self, delta: float, delta_bar_agg: float) -> float:
        lambda_ = self.params['lambda_baseline']
        return (1 + lambda_ * delta) / (1 + lambda_ * delta_bar_agg)

    def best_response_effort(self, delta: float, A: int, W_agg: float, delta_bar_agg: float) -> float:
        if W_agg <= 0: return 0.0
        v = self._get_value(delta)
        g = self._get_novelty_multiplier(delta, delta_bar_agg)
        c_e = self.params['c_e_1'] if A == 1 else self.params['c_e_0']
        return (v * g) / (c_e * W_agg)

    def best_response_differentiation(self, A: int, W_agg: float, delta_bar_agg: float) -> float:
        c_e = self.params['c_e_1'] if A == 1 else self.params['c_e_0']
        
        def phi_function(delta: float) -> float:
            if delta < 0: return np.inf
            v = self._get_value(delta)
            g = self._get_novelty_multiplier(delta, delta_bar_agg)
            e_star = (v * g) / (c_e * W_agg)
            psi = ( (self.params['beta_2'] + self.params['lambda_baseline'] * v / (1 + self.params['lambda_baseline'] * delta_bar_agg)) * g * e_star ) / (self.params['c_delta'] * W_agg)
            return delta - psi

        try:
            delta_star = brentq(phi_function, a=0.0, b=100.0)
        except ValueError:
            delta_star = 0.0

        return max(0, delta_star)

    def _calculate_payoff(self, e: float, delta: float, A: int, W_agg: float, delta_bar_agg: float) -> float:
        v = self._get_value(delta)
        g = self._get_novelty_multiplier(delta, delta_bar_agg)
        s = (e * g) / W_agg if W_agg > 0 else 0.0
        c_e = self.params['c_e_1'] if A == 1 else self.params['c_e_0']
        cost = 0.5 * c_e * e**2 + 0.5 * self.params['c_delta'] * delta**2 + self.params['f_baseline'] * A
        return s * v - cost

    def solve_optimal_strategy(self, W_agg: float, delta_bar_agg: float) -> dict:
        delta_0 = self.best_response_differentiation(A=0, W_agg=W_agg, delta_bar_agg=delta_bar_agg)
        e_0 = self.best_response_effort(delta=delta_0, A=0, W_agg=W_agg, delta_bar_agg=delta_bar_agg)
        payoff_0 = self._calculate_payoff(e=e_0, delta=delta_0, A=0, W_agg=W_agg, delta_bar_agg=delta_bar_agg)

        delta_1 = self.best_response_differentiation(A=1, W_agg=W_agg, delta_bar_agg=delta_bar_agg)
        e_1 = self.best_response_effort(delta=delta_1, A=1, W_agg=W_agg, delta_bar_agg=delta_bar_agg)
        payoff_1 = self._calculate_payoff(e=e_1, delta=delta_1, A=1, W_agg=W_agg, delta_bar_agg=delta_bar_agg)
        
        if payoff_1 >= payoff_0:
            return {'A_star': 1, 'e_star': e_1, 'delta_star': delta_1, 'payoff': payoff_1}
        else:
            return {'A_star': 0, 'e_star': e_0, 'delta_star': delta_0, 'payoff': payoff_0}
