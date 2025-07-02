import os
import pandas as pd
from typing import Dict, List

def save_results_to_csv(results_history: List[Dict], filename: str, output_dir: str = "outputs/tables"):
    """Saves a list of scenario results to a CSV file."""
    if not results_history:
        print("Warning: No results to save.")
        return
    os.makedirs(output_dir, exist_ok=True)
    results_df = pd.DataFrame(results_history)
    if 'Scenario' in results_df.columns:
        results_df.set_index('Scenario', inplace=True)
    filepath = os.path.join(output_dir, filename)
    try:
        results_df.to_csv(filepath)
        print(f"\nResults successfully saved to {filepath}")
    except IOError as e:
        print(f"Error: Could not save results to {filepath}. Reason: {e}")

def print_summary(results_dict: dict, scenario_name: str):
    """Prints a formatted summary of a single scenario's results."""
    print("\n" + "="*50)
    print(f"RESULTS FOR SCENARIO: {scenario_name}")
    print("="*50)
    print("\n--- Welfare Components ---")
    print(f"  Creator Rent:          {results_dict.get('Creator Rent', 0):.4f}")
    print(f"  Platform Profit:       {results_dict.get('Platform Profit', 0):.4f}")
    print(f"  Consumer Surplus:      {results_dict.get('Consumer Surplus', 0):.4f}")
    print(f"  -----------------------------")
    print(f"  Total Welfare:         {results_dict.get('Total Welfare', 0):.4f}")
    print("\n--- Market Characteristics ---")
    print(f"  AI Adoption Rate:      {results_dict.get('AI Adoption Rate', 0):.2%}")
    print(f"  Gini Coefficient:      {results_dict.get('Gini Coefficient', 0):.4f}")
    print(f"  Average Effort:        {results_dict.get('Average Effort', 0):.4f}")
    print(f"  Average Differentiation: {results_dict.get('Average Differentiation', 0):.4f}")
    print("="*50)
