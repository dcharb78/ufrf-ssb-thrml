# Reproduction Protocol

This protocol verifies the core claims using repository scripts.

## 1. Environment

Record the following in your report:

- Date/time:
- OS:
- CPU/GPU:
- Python:
- `jax` version:
- `thrml` version:

Interpreter note:
- This project requires Python 3.10+ for `thrml==0.1.3`.
- If system `python`/`python3` is older, create and use a local virtual environment:

```bash
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is minimal, ensure these are present:

```bash
pip install thrml==0.1.3 jax numpy matplotlib
```

## 2. Quick Smoke Check

```bash
python scripts/quick_demo.py
```

If using the project virtualenv:

```bash
.venv/bin/python scripts/quick_demo.py
```

Pass criteria:
- Script completes without exception.
- Prints exact or near-zero flip deltas in invariance section.
- Produces both `+1` and `-1` outcomes across seeds at least occasionally.

## 3. Core Reproduction Runs

### 3.1 Z2 Invariance

```bash
python scripts/run_invariance.py --m-levels 14 144 --samples 10 --output results/review_invariance.jsonl
```

Virtualenv variant:

```bash
.venv/bin/python scripts/run_invariance.py --m-levels 14 144 --samples 10 --output results/review_invariance.jsonl
```

Expected:
- `Max|dE|` reported as `0.0000000000` for balanced model.
- Output file exists and each row contains:
  - `m_level`, `sample`, `energy_original`, `energy_flipped`, `delta_energy`

### 3.2 Single-Sector SSB

```bash
python scripts/run_single_sector.py --m-level 14 --seeds 50 --output results/review_single_M14.jsonl
```

Virtualenv variant:

```bash
.venv/bin/python scripts/run_single_sector.py --m-level 14 --seeds 50 --output results/review_single_M14.jsonl
```

Expected:
- `Mean |delta_flip|` should be `0.000000` for balanced model.
- Signs should be split around 50/50 over many seeds (not necessarily exact).
- Each run should end with saturated magnetization magnitude near 1 in practice.

### 3.3 Two-Sector Mirror

```bash
python scripts/run_two_sector.py --m-level 14 --seeds 50 --output results/review_two_M14.jsonl
```

Virtualenv variant:

```bash
.venv/bin/python scripts/run_two_sector.py --m-level 14 --seeds 50 --output results/review_two_M14.jsonl
```

Expected:
- `Mean |delta_flip|` should be `0.000000`.
- Anti-correlation can vary by run; verify interpretation is statistical, not deterministic.

## 4. Result Comparison

Compare your metrics to:
- `docs/RESULTS.md`
- `README.md` key result tables
- `results/november_2025/` and `results/february_2026/` baselines

Document:
- Exact metric differences
- Whether differences are within expected sampling fluctuation
- Any regressions in invariance (`delta != 0` is a hard failure)

## 5. Hard Failure Conditions

- Any non-zero `delta_energy` in balanced invariance tests due to logic errors
- Missing or malformed output rows
- Runtime crashes in baseline scripts

## 6. Optional Deeper Checks

- Increase seeds (`--seeds 200`) to tighten confidence intervals
- Re-run with different compute backend and compare drift
- Run additional M-levels (`144`, `1440`) if runtime permits

## 7. Latest Validation Record

- Most recent completed run: `docs/review/REPRO_VALIDATION_2026-03-09.md`
