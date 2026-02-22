#!/usr/bin/env python3
"""
Two-sector mirror SSB test.

Two independent, identical lattices (Sector A and Sector B) evolve separately.
Tests whether vacuum selection is anti-correlated (one picks +1, other picks -1)
and whether total energy is invariant under global sign flip.

Usage:
    python scripts/run_two_sector.py --m-level 14 --seeds 50
"""

import argparse
import json
import os
import sys
import time

os.environ["JAX_PLATFORM_NAME"] = "cpu"
os.environ["JAX_PLATFORMS"] = "cpu"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ufrf_ssb.hamiltonian import build_balanced_model
from ufrf_ssb.sampling import relax, energy, sign_of


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m-level", type=int, default=14)
    parser.add_argument("--seeds", type=int, default=50)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    if args.output is None:
        args.output = f"results/phi4_two_M{args.m_level}.jsonl"
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Two-sector mirror SSB | M={args.m_level} | {args.seeds} seeds")
    records = []
    t0 = time.time()

    for seed in range(args.seeds):
        # Sector A
        model_a, nodes_a, n, _ = build_balanced_model(args.m_level)
        samples_a = relax(model_a, nodes_a, n, seed)
        final_a = samples_a[-1]

        # Sector B (same model, different seed)
        model_b, nodes_b, _, _ = build_balanced_model(args.m_level)
        samples_b = relax(model_b, nodes_b, n, seed + 10000)
        final_b = samples_b[-1]

        e_a = energy(model_a, nodes_a, final_a)
        e_b = energy(model_b, nodes_b, final_b)
        e_a_flip = energy(model_a, nodes_a, 1.0 - final_a)
        e_b_flip = energy(model_b, nodes_b, 1.0 - final_b)

        record = {
            "m_level": args.m_level,
            "seed": seed,
            "energy_total": e_a + e_b,
            "energy_flipped": e_a_flip + e_b_flip,
            "delta_flip": (e_a_flip + e_b_flip) - (e_a + e_b),
            "phi_sign": sign_of(final_a),
            "chi_sign": sign_of(final_b),
        }
        records.append(record)

        if seed % 10 == 0:
            print(f"  {seed}/{args.seeds} phi={record['phi_sign']:+.0f} "
                  f"chi={record['chi_sign']:+.0f} dE={record['delta_flip']:.6f} "
                  f"({time.time()-t0:.1f}s)")

    with open(args.output, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    import numpy as np
    anti = sum(1 for r in records if r["phi_sign"] * r["chi_sign"] < 0)
    n_total = len(records)
    print(f"\nResults ({time.time()-t0:.1f}s):")
    print(f"  Anti-correlated: {anti/n_total*100:.0f}%")
    print(f"  <phi> = {np.mean([r['phi_sign'] for r in records]):.3f}")
    print(f"  <chi> = {np.mean([r['chi_sign'] for r in records]):.3f}")
    print(f"  Mean |delta_flip| = {np.mean([abs(r['delta_flip']) for r in records]):.6f}")
    print(f"  Written to {args.output}")


if __name__ == "__main__":
    main()
