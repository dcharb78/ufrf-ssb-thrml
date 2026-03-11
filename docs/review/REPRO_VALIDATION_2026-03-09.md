# Reproducibility Validation (2026-03-09)

## Scope

Validated `docs/review/REPRODUCTION_PROTOCOL.md` core steps:

1. Quick smoke check
2. Z2 invariance run
3. Single-sector SSB run
4. Two-sector mirror run

## Environment

- Date: 2026-03-09
- OS: macOS-26.3.1-arm64-arm-64bit
- Python used for runs: 3.14.3 (`.venv/bin/python`)
- `jax`: 0.9.1
- `thrml`: 0.1.3
- `numpy`: 2.4.2

## Setup Notes

- System `/usr/bin/python3` is Python 3.9.6 and could not satisfy project requirements.
- A local virtualenv was created at `.venv` using `/opt/homebrew/bin/python3` (3.14.3).
- Dependencies were installed successfully in `.venv`.

## Commands Executed

```bash
.venv/bin/python scripts/quick_demo.py
.venv/bin/python scripts/run_invariance.py --m-levels 14 144 --samples 10 --output results/review_invariance.jsonl
.venv/bin/python scripts/run_single_sector.py --m-level 14 --seeds 50 --output results/review_single_M14.jsonl
.venv/bin/python scripts/run_two_sector.py --m-level 14 --seeds 50 --output results/review_two_M14.jsonl
```

## Outputs Generated

- `results/review_invariance.jsonl` (20 rows)
- `results/review_single_M14.jsonl` (50 rows)
- `results/review_two_M14.jsonl` (50 rows)

## Metrics

### Invariance

- `M=14` max `|delta_energy|`: `0.0`
- `M=144` max `|delta_energy|`: `0.0`
- Verdict: `PASS` (perfect Z2 invariance in balanced model)

### Single-Sector SSB (M=14, n=50)

- `P(+1) = 0.600`
- `P(-1) = 0.400`
- `<sign> = 0.200`
- Mean `|delta_flip| = 0.0`
- Verdict: `PASS` (random vacuum selection with exact flip invariance)

### Two-Sector Mirror (M=14, n=50)

- Anti-correlation: `0.54`
- `<phi> = 0.200`
- `<chi> = -0.160`
- Mean `|delta_flip| = 0.0`
- Verdict: `PASS` (matches expected non-deterministic anti-correlation behavior)

## Comparison vs Existing Docs

Compared against `README.md` and `docs/RESULTS.md`:

- Invariance exactness matches prior claims (`0.0`).
- Single-sector distribution (`0.600 / 0.400`) matches February 2026 values.
- Two-sector anti-correlation (`54%`) matches February 2026 values.

## Final Status

Reproducibility protocol core checks: `PASS`.
