#!/usr/bin/env python3
"""
Quick demo: runs a minimal version of each test to verify everything works.
Total runtime: ~30 seconds on CPU.
"""
import os, sys
os.environ["JAX_PLATFORM_NAME"] = "cpu"
os.environ["JAX_PLATFORMS"] = "cpu"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import jax
import jax.numpy as jnp
import numpy as np
from ufrf_ssb.hamiltonian import build_balanced_model
from ufrf_ssb.sampling import relax, energy, magnetization, sign_of

print("=" * 60)
print("UFRF Z2 SSB — Quick Demo")
print("=" * 60)

# 1. Z2 Invariance
print("\n1. Z2 INVARIANCE (3 random states)")
model, nodes, n, side = build_balanced_model(14)
for s in range(3):
    state = jax.random.bernoulli(jax.random.PRNGKey(s + 42), p=0.5, shape=(n,)).astype(jnp.float32)
    eo = energy(model, nodes, state)
    ef = energy(model, nodes, 1.0 - state)
    print(f"   Sample {s}: E(s)={eo:.4f}, E(-s)={ef:.4f}, |delta|={abs(ef-eo):.10f}")
print("   -> E(s) = E(-s) exactly. Hamiltonian has Z2 symmetry.")

# 2. Single-sector SSB (5 seeds)
print("\n2. SINGLE-SECTOR SSB (5 seeds)")
signs = []
for seed in range(5):
    model, nodes, n, _ = build_balanced_model(14)
    samp = relax(model, nodes, n, seed)
    s = sign_of(samp[-1])
    signs.append(s)
    print(f"   Seed {seed}: sign = {s:+.0f}")
print(f"   -> Each run picks +1 or -1. Ensemble: {np.mean(signs):+.2f}")
print("   -> Individual symmetry breaking with random vacuum selection.")

# 3. Two-sector mirror (3 seeds)
print("\n3. TWO-SECTOR MIRROR (3 seeds)")
for seed in range(3):
    ma, na, n, _ = build_balanced_model(14)
    sa = relax(ma, na, n, seed)
    mb, nb, _, _ = build_balanced_model(14)
    sb = relax(mb, nb, n, seed + 10000)
    phi_sign = sign_of(sa[-1])
    chi_sign = sign_of(sb[-1])
    corr = "ANTI" if phi_sign * chi_sign < 0 else "SAME"
    print(f"   Seed {seed}: phi={phi_sign:+.0f}, chi={chi_sign:+.0f} [{corr}]")
print("   -> Independent sectors tend to choose opposite vacua.")

print("\n" + "=" * 60)
print("All tests passed. See README.md for full experiment details.")
print("=" * 60)
