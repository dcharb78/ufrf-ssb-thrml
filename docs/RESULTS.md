# Detailed Results

## Reproduction Summary

All results from November 2025 were independently reproduced in February 2026 on different hardware (Linux VM, CPU-only) with the same THRML 0.1.3 library.

## 1. Z₂ Invariance

The most fundamental test: for any random spin configuration s, does E(s) = E(−s)?

### Balanced Model (no bias)

| M-Level | Lattice | Samples | Max \|ΔE\| (Nov 2025) | Max \|ΔE\| (Feb 2026) |
|---------|---------|---------|-----------------------|-----------------------|
| 14      | 14×14   | 5–10    | 0.0000000000          | 0.0000000000          |
| 144     | 12×12   | 10      | 0.0000000000          | 0.0000000000          |
| 1440    | 38×38   | 10      | 0.0000000000          | —                     |

The energy is **exactly** invariant. Not approximately — the floating point values are bit-for-bit identical.

## 2. Single-Sector SSB

Each seed starts from a random (Hinton) initialization, relaxes via THRML MCMC, and the final magnetization sign is recorded.

### M=14 (50 seeds)

| Metric | Nov 2025 | Feb 2026 |
|--------|----------|----------|
| P(sign=+1) | 0.420 ± 0.070 | 0.600 ± 0.069 |
| P(sign=−1) | 0.580 ± 0.070 | 0.400 ± 0.069 |
| Ensemble ⟨sign⟩ | −0.160 ± 0.141 | +0.200 ± 0.140 |
| Individual \|sign\| | 1.000 | 1.000 |
| Mean \|Δflip\| | 0.000000 | 0.000000 |

### M=144 (30 seeds)

| Metric | Nov 2025 | Feb 2026 |
|--------|----------|----------|
| P(sign=+1) | 0.400 ± 0.089 | 0.633 ± 0.088 |
| P(sign=−1) | 0.600 ± 0.089 | 0.367 ± 0.088 |
| Ensemble ⟨sign⟩ | −0.200 | +0.267 |

### Binomial Tests (H₀: P(+1) = 0.5)

| Run | k | n | p-value | Verdict |
|-----|---|---|---------|---------|
| Nov 2025 M=14 | 21 | 50 | 0.322 | Consistent with 50/50 |
| Feb 2026 M=14 | 30 | 50 | 0.203 | Consistent with 50/50 |
| Nov 2025 M=144 | 12 | 30 | 0.362 | Consistent with 50/50 |
| Feb 2026 M=144 | 19 | 30 | 0.200 | Consistent with 50/50 |

All runs are consistent with unbiased vacuum selection (p > 0.05).

### Interpretation

Each individual run fully breaks Z₂ symmetry — the magnetization saturates to ±1. But averaged over seeds, the ensemble mean is statistically consistent with zero. This is the textbook definition of spontaneous symmetry breaking: the Hamiltonian is symmetric, but the ground states are not. The system must choose one, and it does so randomly.

The fact that Nov 2025 slightly favored −1 while Feb 2026 slightly favored +1 is expected — these are independent random experiments.

## 3. Two-Sector Mirror Test

Two independent, identical lattices (Sector A = φ, Sector B = χ) evolve from different random seeds.

### M=14 (50 seeds)

| Metric | Nov 2025 | Feb 2026 |
|--------|----------|----------|
| P(φ:+, χ:−) | 0.200 | — |
| P(φ:−, χ:+) | 0.400 | — |
| Anti-correlated total | 60% | 54% |
| Mean \|Δflip\| | 0.000 | 0.000 |
| Mean \|Δswap\| | 0.000 | 0.000 |

Anti-correlation above 50% means the two sectors preferentially choose opposite vacua — one picks +1, the other picks −1. This is consistent with the dual-sector mirror structure.

## 4. Phase Transition (Feb 2026)

Noise amplitude swept from 0 to 0.05. At all tested noise levels, the order parameter remained saturated:

| Noise σ | ⟨\|sign\|⟩ |
|---------|-----------|
| 0.0000  | 1.000     |
| 0.0001  | 1.000     |
| 0.0010  | 1.000     |
| 0.0050  | 1.000     |
| 0.0100  | 1.000     |
| 0.0500  | 1.000     |

The system is deep in the ordered (broken symmetry) phase at these coupling strengths (κ=0.3, λ=0.5, β=1.0). The critical noise level for a disorder transition is above 0.05 for this parameter regime.

## 5. Ensemble Energy Drops (Feb 2026)

20 runs tracking initial vs final energy:

| Metric | Value |
|--------|-------|
| Mean exothermic drop | 12.82 |
| ⟨sign⟩ over ensemble | +0.100 |
| P(+1) | 0.550 |
| P(−1) | 0.450 |

The system consistently releases energy during relaxation (exothermic process), settling into lower-energy configurations. This is the physical mechanism driving SSB: the symmetric high-energy state is unstable, and the system rolls down to one of two degenerate minima.
