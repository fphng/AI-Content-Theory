from scipy.stats import beta

# --- Model Primitives ---
PARAMS = {
    'beta_0': 0.1, 'beta_1': 1.0, 'beta_2': 1.5,
    'c_e_0': 1.0,  # Cost for human
    'c_e_1': 0.38, # Cost for AI
    'c_delta': 1.0,
    'f_baseline': 5.0,
    'gamma': 1.0,
    'lambda_baseline': 0.05,
    'eta': 0.15,   # Platform margin
    'kappa': 0.35, # Consumer surplus weight
}

# --- Simulation Settings ---
SIM_SETTINGS = {
    'num_creators': 1000, # Number of points for numerical integration
    'talent_distribution': beta(2, 2),
    'solver_tolerance': 1e-6,
    'max_iterations': 100
}
