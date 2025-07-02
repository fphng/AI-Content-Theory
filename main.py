# F. Nguyen (2025) - Emory
import copy
import pandas as pd
from config import PARAMS, SIM_SETTINGS
from src.equilibrium_solver import find_equilibrium
from src.welfare import run_welfare_analysis
from src.utils import print_summary, save_results_to_csv
from src.plotting import plot_welfare_decomposition, plot_market_characteristics

def main():
    """
    Main function to run the creator economy simulation.
    """
    
    # --- 1. Define Policy Scenarios ---
    scenario_a = {'name': 'Baseline', 'params': copy.deepcopy(PARAMS)}

    params_b = copy.deepcopy(PARAMS)
    params_b['f_baseline'] *= 0.20
    scenario_b = {'name': 'OpenAI Price Cut (Δf)', 'params': params_b}

    params_c = copy.deepcopy(params_b)
    params_c['lambda_baseline'] *= 1.05
    scenario_c = {'name': '+ EU AI Act (Δλ)', 'params': params_c}

    params_d = copy.deepcopy(params_c)
    params_d['c_delta'] *= 0.90
    scenario_d = {'name': '+ Originality Subsidy (Δc_δ)', 'params': params_d}

    scenarios = [scenario_a, scenario_b, scenario_c, scenario_d]
    results_history = []

    # --- 2. Run Simulation Loop ---
    for scenario in scenarios:
        print(f"\n{'='*20} RUNNING SCENARIO: {scenario['name']} {'='*20}")
        equilibrium_df, W_eq, _ = find_equilibrium(scenario['params'], SIM_SETTINGS)

        if equilibrium_df is None:
            print(f"Could not find equilibrium for scenario: {scenario['name']}")
            continue

        welfare_results = run_welfare_analysis(equilibrium_df, W_eq, scenario['params'])
        print_summary(welfare_results, scenario['name'])
        welfare_results['Scenario'] = scenario['name']
        results_history.append(welfare_results)

    # --- 3. Save and Plot Final Results ---
    if results_history:
        final_results_df = pd.DataFrame(results_history)
        save_results_to_csv(final_results_df, filename='simulation_summary_table.csv')
        plot_welfare_decomposition(final_results_df)
        plot_market_characteristics(final_results_df)

if __name__ == "__main__":
    main()
