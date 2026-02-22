#!/usr/bin/env python3
"""
Z2 invariance verification across M-levels.

For each M-level, generates random spin configurations and verifies
that E(s) = E(-s) exactly. This is the most fundamental test:
if delta != 0, the Hamiltonian has a bug.

Usage:
    python scripts/run_invariance.py --m-levels 14 144
    python scripts/run_invariance.py --m-levels 14 144 1440 --samples 20
"""

import argparse
import json
import os
import sys
import time

os.environ["JAX_PLATFORM_NAME"] = "cpu"
os.environ["JAX_PLATFORMS"] = "cpu"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jax
import jax.numpy as jnp

from ufrf_ssb.hamiltonian import build_balanced_model, lattice_side
from ufrf_ssb.sampling import energy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m-levels", type=int, nargs="+", default=[14, 144])
    parser.add_argument("--samples", type=int, default=10)
    parser.add_argument("--output", type=str, default="results/invariance.jsonl")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    print(f"Z2 invariance test | M={args.m_levels} | {args.samples} samples each")

    records = []
    for m in args.m_levels:
        side = lattice_side(m)
        n = side * side
        t0 = time.time()
        print(f"\n  M={m} ({side}x{side} = {n} nodes)...")

        for s in range(args.samples):
            model, nodes, nn, _ = build_balanced_model(m)
            key = jax.random.PRNGKey(s + 42)
            state = jax.random.bernoulli(key, p=0.5, shape=(nn,)).astype(jnp.float32)
            e_orig = energy(model, nodes, state)
            e_flip = energy(model, nodes, 1.0 - state)
            delta = e_flip - e_orig
            records.append({
                "m_level": m, "sample": s,
                "energy_original": e_orig, "energy_flipped": e_flip,
                "delta_energy": delta,
            })

        deltas = [abs(r["delta_energy"]) for r in records if r["m_level"] == m]
        mx = max(deltas)
        print(f"  M={m}: Max|dE| = {mx:.10f} "
              f"{'PERFECT Z2' if mx == 0 else 'BROKEN'} ({time.time()-t0:.1f}s)")

    with open(args.output, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"\nWritten to {args.output}")


if __name__ == "__main__":
    main()
