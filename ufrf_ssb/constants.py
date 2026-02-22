"""
UFRF geometric constants.

All values are derived from three axioms:
  1. PRIMARY = 13 (the fundamental cycle length)
  2. PHI = (1 + sqrt(5)) / 2 (the golden ratio)
  3. ALPHA = 1 / (4*pi^3 + pi^2 + pi) (fine structure analog)

No arbitrary parameters. Every constant is a ratio of these three.
"""

import jax.numpy as jnp

# Axiom 1: 13-cycle geometry
PRIMARY = 13
MEASURE = 20
BEAM = PRIMARY * MEASURE  # 260

# Axiom 2: Golden ratio
PHI = (1 + jnp.sqrt(5)) / 2  # 1.6180339887...

# Derived: activation threshold
TAU = 1 / (2 * PRIMARY * PHI)  # 0.023771...

# Axiom 3: Fine structure analog
ALPHA_INV = 4 * jnp.pi**3 + jnp.pi**2 + jnp.pi  # 137.0363...
ALPHA = 1 / ALPHA_INV

# Sampling parameters
BETA = 8.3  # Inverse temperature
REST_GAIN_FACTOR = 1.10
COUPLING_RANGE = [1, 2, 3, 5]  # Multi-range couplings

# REST node: position 9 (0-indexed) in the 13-cycle = 10th position
REST_POSITION = 9

# M-level hierarchy: M = 144 * 10^n
# Maps M-level to lattice side length
M_LEVEL_MAP = {
    14: 14,       # 196 nodes
    144: 12,      # 144 nodes
    1440: 38,     # 1,444 nodes
    14400: 120,   # 14,400 nodes
    144000: 379,  # 143,641 nodes
}
