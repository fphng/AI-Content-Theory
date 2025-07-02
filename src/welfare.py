import numpy as np
import pandas as pd

def calculate_gini(incomes: np.ndarray) -> float:
    """Calculates the Gini coefficient for a list of incomes."""
    incomes = np.asarray(incomes, dtype=float)
    if incomes.size == 0 or np.sum(np.abs(incomes)) == 0:
        return 0.0
    incomes = np.sort(incomes)
    n = len(incomes)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * incomes)) / (n * np.sum(incomes))

def run_welfare_analysis(equilibrium_df: pd.DataFrame, W_eq: float, params: dict) -> dict:
    """Calculates all welfare components from a solved equilibrium."""
    creator_rent = equilibrium_df['payoff'].mean()
    platform_profit = params['eta'] * W_eq

    if W_eq > 0:
        equilibrium_df['s'] = equilibrium_df['w'] / W_eq
    else:
        equilibrium_df['s'] = 0

    equilibrium_df['v'] = params['beta_0'] + params['beta_1'] * equilibrium_df['theta'] + params['beta_2'] * equilibrium_df['delta_star']
    consumer_surplus_base = (equilibrium_df['s'] * equilibrium_df['v']).mean()
    consumer_surplus = params['kappa'] * consumer_surplus_base
    
    total_welfare = creator_rent + platform_profit + consumer_surplus
    gini_coefficient = calculate_gini(equilibrium_df['payoff'].to_numpy())
    ai_adoption_rate = equilibrium_df['A_star'].mean()
    avg_effort = equilibrium_df['e_star'].mean()
    avg_differentiation = equilibrium_df['delta_star'].mean()

    results = {
        'Creator Rent': creator_rent,
        'Platform Profit': platform_profit,
        'Consumer Surplus': consumer_surplus,
        'Total Welfare': total_welfare,
        'Gini Coefficient': gini_coefficient,
        'AI Adoption Rate': ai_adoption_rate,
        'Average Effort': avg_effort,
        'Average Differentiation': avg_differentiation
    }
    return results
