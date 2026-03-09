# UFRF Spontaneous Symmetry Breaking on THRML

**Z₂-symmetric Ising lattice with non-trivial 13-cycle topology, tested via Extropic's thermodynamic sampling library.**

## What This Is

A Z₂-symmetric Hamiltonian on 2D square lattices with a structured coupling topology inspired by the Universal Field Resonance Framework (UFRF). The system uses [Extropic's THRML library](https://github.com/extropic-ai/thrml) for thermodynamic MCMC sampling on `IsingEBM` models.

The coupling topology is not random or uniform — it has a 13-position cyclic structure with designated REST nodes (position 10 in each cycle) that receive enhanced coupling strength proportional to √φ. Nearest-neighbor couplings are modulated by REST proximity. No bias terms are present, ensuring exact Z₂ symmetry: **E(s) = E(−s)**.

## Key Result

Starting from random initial configurations, the system spontaneously selects one of two degenerate ground states — textbook spontaneous symmetry breaking. The critical result is that the energy invariance under global spin flip is **exactly zero** (not approximately — exactly), verified at three orders of magnitude in lattice size.

| M-Level | Lattice | Nodes | Max \|ΔE\| under s → −s |
|---------|---------|-------|------------------------|
| 14      | 14×14   | 196   | **0.0000000000**       |
| 144     | 12×12   | 144   | **0.0000000000**       |
| 1440    | 38×38   | 1,444 | **0.0000000000**       |

Single-sector vacuum selection (50 seeds at M=14):
- P(+1) = 0.42–0.60 depending on run batch
- P(−1) = 0.40–0.58
- All batches consistent with 50/50 (binomial p > 0.20)
- **Every individual run breaks symmetry** (|magnetization| ≈ 1.0)
- **Ensemble average is zero** within statistical error

Two-sector mirror test (50 seeds): 54–60% anti-correlated vacuum selection between independent sectors with identical physics.

## Results from the Experiments

The experiment was originally run in November 2025 and independently reproduced in February 2026 on different hardware with the same THRML library version (0.1.3):

| Metric | Nov 2025 | Feb 2026 |
|--------|----------|----------|
| Z₂ invariance ΔE | 0.000000 | 0.000000 |
| Individual \|sign\| | 1.000 | 1.000 |
| P(+1) M=14 | 0.420 ± 0.070 | 0.600 ± 0.069 |
| Anti-correlated % | 60% | 54% |
| φ⁴ ↔ UFRF δ_flip | 0.000000 | 0.000000 |

Both runs are consistent with each other and with the null hypothesis of unbiased vacuum selection.

### What these results show

- **Exact Z₂ symmetry of the Hamiltonian:** global spin flip leaves the energy unchanged to machine precision (ΔE = 0.000000 in all tested balanced configurations).
- **Spontaneous symmetry breaking per trajectory:** each individual run settles to a fully ordered vacuum (\|sign\| = 1.000), choosing either +1 or −1.
- **No ensemble bias:** across seeds, +1 and −1 frequencies remain statistically consistent with 50/50.
- **Cross-run reproducibility:** independently collected Nov 2025 and Feb 2026 datasets agree on all core physics conclusions.

## The Coupling Topology

What makes this different from a standard Ising model:

**13-cycle breathing structure.** Each group of 13 nodes forms a cycle with position-dependent coupling modulation. Positions 0–5 are in the "expansion" phase; positions 6–12 are in the "contraction" phase (multiplied by −1/φ ≈ −0.618).

**REST nodes.** Position 9 (the 10th in each cycle) receives a coupling boost of √φ × (1 + τ) × 1.10, where τ = 1/(2 × 13 × φ) ≈ 0.0238. REST nodes also form long-range connections to all other REST nodes in the lattice.

**Multi-range couplings.** Each node couples to neighbors at distances [1, 2, 3, 5] (a Fibonacci-like set), not just nearest neighbors.

**M-level hierarchy.** The lattice size maps to the UFRF hierarchy: M=14 → 14×14, M=144 → 12×12, M=1440 → 38×38, M=144000 → 379×379.

Despite this non-trivial topology, the Hamiltonian maintains exact Z₂ symmetry because all coupling terms are quadratic (s_i × s_j) with no linear bias.

## UFRF Constants

All derived from three values: PRIMARY=13, φ=(1+√5)/2, α=1/(4π³+π²+π).

| Constant | Value | Origin |
|----------|-------|--------|
| PHI | 1.6180339887... | Golden ratio |
| TAU | 0.0237714... | 1/(2 × 13 × φ) |
| ALPHA | 0.0072973... | 1/(4π³ + π² + π) |
| REST position | 9 (mod 13) | 10th position in cycle |
| Contraction | −0.618034 | −1/φ |

## Quick Start

```bash
pip install thrml==0.1.3 jax matplotlib numpy

# Verify Z₂ invariance
python scripts/run_invariance.py --m-levels 14 144

# Run single-sector SSB (50 seeds)
python scripts/run_single_sector.py --m-level 14 --seeds 50

# Run two-sector mirror test
python scripts/run_two_sector.py --m-level 14 --seeds 50
```

Results are written as JSONL to the `results/` directory.

## Repository Structure

```
ufrf-ssb-thrml/
├── ufrf_ssb/
│   ├── __init__.py
│   ├── constants.py          # UFRF geometric constants
│   ├── hamiltonian.py        # Z₂-symmetric model builders
│   └── sampling.py           # THRML relaxation + observables
├── scripts/
│   ├── run_single_sector.py  # Single-sector SSB test
│   ├── run_two_sector.py     # Two-sector mirror test
│   └── run_invariance.py     # Z₂ invariance verification
├── results/
│   ├── november_2025/        # Original results (50 seeds)
│   └── february_2026/        # Independent reproduction
├── docs/
│   └── RESULTS.md            # Detailed comparison tables
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- JAX (any recent version)
- THRML 0.1.3 (`pip install thrml==0.1.3`)
- NumPy, Matplotlib

## Why THRML

[Extropic](https://extropic.ai) is building thermodynamic computing hardware — physical chips where Boltzmann sampling happens in the physics of the device, not in software. THRML is their software library that provides the same sampling interface. Running UFRF lattice models on THRML means the identical Hamiltonian could be ported to Extropic hardware with no algorithmic changes — only the sampling backend changes from MCMC to physical thermodynamics.

## License

MIT

## Author

Daniel Charboneau (daniel@charboneau.us)
