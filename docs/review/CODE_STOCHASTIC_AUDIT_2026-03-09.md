# Code Stochastic Audit (Targeted, 2026-03-09)

## Scope

Audited files:
- `ufrf_ssb/hamiltonian.py`
- `ufrf_ssb/sampling.py`
- `scripts/run_invariance.py`
- `scripts/run_two_sector.py`

Focus areas:
1. bond normalization
2. PRNG key splitting/usage
3. dtype precision in energy path
4. magnetization/sign implementation
5. THRML relaxation schedule usage

## Methods

- Static review of implementation logic.
- Runtime probes in `.venv`:
  - edge multiplicity/weight checks on balanced models (`M=14`, `M=144`)
  - JAX precision mode probe
  - JSONL schema integrity checks on generated review outputs

## Probe Results

### 1) Bond normalization / graph construction

Findings:
- Directed edge count is exactly `4n` for balanced models.
- Unique undirected edges are exactly `2n`.
- Every undirected edge appears exactly twice (`(i,j)` and `(j,i)`), no irregular multiplicities observed.

Observed runtime evidence:
- `M=14`: directed `784`, unique undirected `392`, multiplicity `2`
- `M=144`: directed `576`, unique undirected `288`, multiplicity `2`

Assessment:
- Construction is internally consistent.
- Remaining risk is backend semantics: if THRML ever changes directed-edge energy interpretation, normalization assumptions should be re-validated.

### 2) PRNG handling

Findings:
- `sampling.relax()` splits key once into initialization and sampling streams.
- `run_two_sector.py` uses deterministic distinct seeds (`s`, `s+10000`) for sectors.
- `run_invariance.py` uses deterministic per-sample keys (`s+42`), enabling reproducibility.

Assessment:
- No accidental key reuse bug found in audited paths.

### 3) Dtype precision and energy path

Findings:
- Model weights/biases/beta use `float32`.
- Runtime mode shows `jax_enable_x64 = False`.
- Balanced invariance remained exactly zero in reproduced tests, but numeric margin for larger/future variants remains `float32`-bound.

Assessment:
- Current behavior is stable for audited runs.
- Precision policy should be documented explicitly as a design choice.

### 4) Magnetization and sign

Findings:
- `magnetization()` correctly maps `{0,1} -> {-1,+1}` and averages.
- `sign_of()` returns `0` when magnetization is exactly zero.

Assessment:
- Implementation is correct.
- Downstream analyses should explicitly state how tie states (`0`) are handled, even if rare in current runs.

### 5) THRML schedule / relaxation logic

Findings:
- Schedule is explicit and stable (`warmup=50`, `n_samples=200`, `steps_per=3`).
- Even/odd block update program is clearly defined.
- Script-level defaults depend on this schedule implicitly.

Assessment:
- Logic is coherent and deterministic given seeds.
- For reproducibility, schedule parameters should be surfaced and recorded in result metadata when runs are published.

## Script Reliability Checks

JSONL schema checks passed for:
- `results/review_invariance.jsonl` (20 rows)
- `results/review_single_M14.jsonl` (50 rows)
- `results/review_two_M14.jsonl` (50 rows)

## Findings (Prioritized)

| Severity | File:Line | Finding | Impact | Recommendation |
|----------|-----------|---------|--------|----------------|
| Low | `ufrf_ssb/hamiltonian.py:79` | Directed edge duplication depends on backend edge semantics. | Potential drift risk if backend behavior changes. | Keep multiplicity unit test and add an explicit backend-contract note in docs/changelog during upgrades. |

## Fixes Applied (2026-03-09)

- `m_level` validation:
  - `lattice_side()` now raises on unsupported levels.
  - `run_invariance.py`, `run_single_sector.py`, and `run_two_sector.py` now fail fast with clear supported-level messages.
- schedule metadata persistence:
  - Added CLI args `--warmup`, `--n-samples`, `--steps-per` to single/two-sector scripts.
  - Added `schedule_warmup`, `schedule_n_samples`, `schedule_steps_per` to JSONL rows.
- normalization guard:
  - Added deterministic unit tests in `tests/test_balanced_model_construction.py`:
    - exact directed/undirected multiplicity checks
    - positive-weight check in default balanced regime

## Verdict

`PASS`

No blocking correctness defect was found in the audited code paths. Previously identified medium/low issues were resolved; one low-severity backend-upgrade risk remains and is now guarded by tests.
