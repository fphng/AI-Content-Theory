import numpy as np
import pandas as pd
from .creator import Creator

def find_equilibrium(params: dict, sim_settings: dict) -> tuple[pd.DataFrame, float, float]:
    """
    Solves for the market equilibrium using a fixed-point iteration algorithm.
    """
    num_creators = sim_settings['num_creators']
    dist = sim_settings['talent_distribution']
    quantiles = np.linspace(0.001, 0.999, num_creators)
    theta_grid = dist.ppf(quantiles)

    W_guess = 1.0
    delta_bar_guess = 0.5
    damping = 0.6 

    print("--- Starting Equilibrium Solver ---")
    print(f"Initial Guess: W={W_guess:.4f}, δ̄={delta_bar_guess:.4f}")

    for i in range(sim_settings['max_iterations']):
        results_list = []
        for theta in theta_grid:
            creator = Creator(talent_theta=theta, params=params)
            strategy = creator.solve_optimal_strategy(W_agg=W_guess, delta_bar_agg=delta_bar_guess)
            strategy['theta'] = theta
            results_list.append(strategy)

        eq_df = pd.DataFrame(results_list)
        lambda_ = params['lambda_baseline']
        eq_df['g'] = (1 + lambda_ * eq_df['delta_star']) / (1 + lambda_ * delta_bar_guess)
        eq_df['w'] = eq_df['e_star'] * eq_df['g']

        W_new = eq_df['w'].mean()
        delta_bar_new = eq_df['delta_star'].mean()

        W_diff = abs(W_new - W_guess)
        delta_diff = abs(delta_bar_new - delta_bar_guess)

        print(f"Iter {i+1:02d}: W={W_new:.4f} (Δ={W_diff:.6f}), δ̄={delta_bar_new:.4f} (Δ={delta_diff:.6f})")

        if W_diff < sim_settings['solver_tolerance'] and delta_diff < sim_settings['solver_tolerance']:
            print(f"\nConvergence reached after {i+1} iterations.")
            return eq_df, W_new, delta_bar_new

        W_guess = damping * W_guess + (1 - damping) * W_new
        delta_bar_guess = damping * delta_bar_guess + (1 - damping) * delta_bar_new

    print(f"\nWarning: Solver did not converge within {sim_settings['max_iterations']} iterations.")
    return eq_df, W_new, delta_bar_new
