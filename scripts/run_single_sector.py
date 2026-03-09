#!/usr/bin/env python3
"""
Single-sector SSB test.

For each seed, builds a Z2-symmetric balanced model, runs THRML relaxation,
and records the sign of the final magnetization and the energy invariance
under spin flip.

Usage:
    python scripts/run_single_sector.py --m-level 14 --seeds 50
    python scripts/run_single_sector.py --m-level 144 --seeds 30
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
from ufrf_ssb.constants import M_LEVEL_MAP
from ufrf_ssb.sampling import relax, energy, magnetization, sign_of


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m-level", type=int, default=14)
    parser.add_argument("--seeds", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=50)
    parser.add_argument("--n-samples", type=int, default=200)
    parser.add_argument("--steps-per", type=int, default=3)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    if args.m_level not in M_LEVEL_MAP:
        known = ", ".join(str(k) for k in sorted(M_LEVEL_MAP))
        parser.error(
            f"Unsupported m-level: {args.m_level}. Supported levels: {known}"
        )

    if args.output is None:
        args.output = f"results/phi4_single_M{args.m_level}.jsonl"

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Single-sector SSB | M={args.m_level} | {args.seeds} seeds")
    records = []
    t0 = time.time()

    for seed in range(args.seeds):
        model, nodes, n, side = build_balanced_model(args.m_level)
        samples = relax(
            model,
            nodes,
            n,
            seed,
            warmup=args.warmup,
            n_samples=args.n_samples,
            steps_per=args.steps_per,
        )
        final = samples[-1]
        flipped = 1.0 - final

        e_orig = energy(model, nodes, final)
        e_flip = energy(model, nodes, flipped)

        record = {
            "m_level": args.m_level,
            "seed": seed,
            "energy_original": e_orig,
            "energy_flipped": e_flip,
            "delta_flip": e_flip - e_orig,
            "sign": sign_of(final),
            "magnetization": magnetization(final),
            "schedule_warmup": args.warmup,
            "schedule_n_samples": args.n_samples,
            "schedule_steps_per": args.steps_per,
        }
        records.append(record)

        if seed % 10 == 0:
            print(f"  {seed}/{args.seeds} sign={record['sign']:+.0f} "
                  f"dE={record['delta_flip']:.6f} ({time.time()-t0:.1f}s)")

    # Write results
    with open(args.output, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    # Summary
    signs = [r["sign"] for r in records]
    n_total = len(signs)
    pos = sum(1 for s in signs if s > 0)
    neg = sum(1 for s in signs if s < 0)
    import numpy as np
    print(f"\nResults ({time.time()-t0:.1f}s):")
    print(f"  P(+1) = {pos/n_total:.3f}")
    print(f"  P(-1) = {neg/n_total:.3f}")
    print(f"  <sign> = {np.mean(signs):.3f}")
    print(f"  Mean |delta_flip| = {np.mean([abs(r['delta_flip']) for r in records]):.6f}")
    print(f"  Written to {args.output}")


if __name__ == "__main__":
    main()
