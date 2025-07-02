# Scale or Stand Out? - Official Simulation Package

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the official Python simulation package for the research paper, **"Scale or Stand Out? Content Strategy and Welfare in the Age of Generative AI."**

This package implements the closed-form contest model described in the paper, allowing researchers to replicate the findings and explore new policy counterfactuals.

## Overview

The simulation models a creator economy where a continuum of creators, heterogeneous in talent, strategically choose their effort, level of content differentiation, and whether to adopt generative AI. The platform allocates finite user attention based on a rule that rewards both effort and content novelty.

This package is designed to find the market equilibrium under different policy regimes and analyze the resulting impact on social welfare, creator income, and market concentration.

### Features

* **Equilibrium Solver**: Implements a fixed-point iteration algorithm to find the Bayesian-Nash equilibrium of the creator contest.
* **Welfare Analysis**: Calculates all key welfare components, including creator rent, consumer surplus, and platform profit.
* **Inequality Metrics**: Computes the Gini coefficient on creator income to analyze the distributional effects of policy shocks.
* **Scenario Management**: Easily configurable to run the specific policy shocks analyzed in the paper.
* **Extensible**: Designed modularly to allow for the easy addition of new parameters, creator behaviors, or policy levers.

## Project Structure

/ai-creator-economy-sim/
|
├── main.py
├── config.py
├── requirements.txt
├── README.md
|
├── src/
│   ├── init.py
│   ├── creator.py
│   ├── equilibrium_solver.py
│   ├── welfare.py
│   └── utils.py
│   └── plotting.py
|
└── outputs/
├── tables/
└── figures/

## Requirements

* Python 3.9+
* NumPy
* SciPy
* Pandas
* Matplotlib

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/ai-creator-economy-sim.git](https://github.com/your-username/ai-creator-economy-sim.git)
    cd ai-creator-economy-sim
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Simulation

1.  **Navigate to the project's root directory.**
2.  **Execute the main script:**
    ```bash
    python main.py
    ```

After all scenarios have completed, a summary table will be saved to `outputs/tables/simulation_summary_table.csv`, and plots will be saved in `outputs/figures/`.

