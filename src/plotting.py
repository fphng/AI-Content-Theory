## Visualization

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_welfare_decomposition(results_df: pd.DataFrame, output_dir: str = "outputs/figures"):
    """Creates and saves a stacked bar chart of welfare components across scenarios."""
    if 'Scenario' not in results_df.columns:
        results_df = results_df.reset_index()
    if 'Scenario' not in results_df.columns:
        print("Warning: 'Scenario' column not found. Cannot plot.")
        return
        
    plot_df = results_df.set_index('Scenario')
    welfare_components = ['Creator Rent', 'Platform Profit', 'Consumer Surplus']
    if not all(col in plot_df.columns for col in welfare_components):
        print("Warning: DataFrame is missing required welfare components. Cannot plot.")
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['#0072B2', '#D55E00', '#009E73']
    
    bottom = np.zeros(len(plot_df))
    for i, component in enumerate(welfare_components):
        ax.bar(plot_df.index, plot_df[component], bottom=bottom, label=component, color=colors[i])
        bottom += plot_df[component].values

    ax.set_title('Welfare Decomposition Across Policy Scenarios', fontsize=16, pad=20)
    ax.set_ylabel('Welfare (Normalized)', fontsize=12)
    ax.set_xlabel('Scenario', fontsize=12)
    ax.tick_params(axis='x', rotation=15, labelsize=10)
    ax.legend(title='Welfare Component', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.5, label='Baseline Welfare')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title='Welfare Component', fontsize=10)
    
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "welfare_decomposition.png")
    plt.savefig(filepath, dpi=300)
    print(f"\nPlot successfully saved to {filepath}")
    plt.close(fig)

def plot_market_characteristics(results_df: pd.DataFrame, output_dir: str = "outputs/figures"):
    """Creates and saves bar charts for AI adoption and Gini coefficient."""
    if 'Scenario' not in results_df.columns:
        results_df = results_df.reset_index()
    if 'Scenario' not in results_df.columns:
        print("Warning: 'Scenario' column not found. Cannot plot.")
        return

    plot_df = results_df.set_index('Scenario')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    plot_df['AI Adoption Rate'].plot(kind='bar', ax=ax1, color='#4682B4')
    ax1.set_title('AI Adoption Rate by Scenario', fontsize=14)
    ax1.set_ylabel('Adoption Rate', fontsize=12)
    ax1.set_xlabel('')
    ax1.tick_params(axis='x', rotation=25, labelsize=10, ha='right')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    plot_df['Gini Coefficient'].plot(kind='bar', ax=ax2, color='#D2691E')
    ax2.set_title('Creator Income Inequality by Scenario', fontsize=14)
    ax2.set_ylabel('Gini Coefficient', fontsize=12)
    ax2.set_xlabel('')
    ax2.tick_params(axis='x', rotation=25, labelsize=10, ha='right')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.set_ylim(bottom=min(0.40, plot_df['Gini Coefficient'].min() - 0.01))

    fig.suptitle('Market Characteristics Across Scenarios', fontsize=18, y=1.02)
    plt.tight_layout()
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "market_characteristics.png")
    plt.savefig(filepath, dpi=300)
    print(f"Plot successfully saved to {filepath}")
    plt.close(fig)
