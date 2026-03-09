# Code Quality Checklist

Review these areas and record findings with file/line references.

## 1. Architecture and Separation

- [x] Clear separation of constants, model construction, and sampling
- [x] Scripts are thin orchestration layers, not logic-heavy
- [x] Public API in `ufrf_ssb/__init__.py` matches actual usage

## 2. Correctness: Hamiltonian Construction

Files: `ufrf_ssb/hamiltonian.py`, `ufrf_ssb/constants.py`

- [x] `build_balanced_model()` has zero biases
- [x] Couplings are symmetric and added in both directions intentionally
- [x] Periodic boundary conditions are correctly implemented
- [x] REST weighting matches documented equations
- [x] M-level to lattice mapping is explicit and consistent with docs

## 3. Correctness: Sampling and Observables

File: `ufrf_ssb/sampling.py`

- [x] Relaxation schedule parameters are sensible and documented
- [x] `magnetization()` correctly maps `{0,1}` to `{-1,+1}`
- [x] `sign_of()` behavior for exact zero magnetization is acceptable
- [x] Energy helper matches model expectations

## 4. Script Reliability

Files: `scripts/*.py`

- [x] Default outputs are safe and deterministic
- [x] CLI args have reasonable defaults and validation
- [x] Progress logs are informative for long runs
- [x] JSONL output always writes one valid JSON object per line

## 5. Numerical and JAX/THRML Concerns

- [x] Dtype choices are explicit where needed (`float32`/`float64`)
- [x] PRNG key usage avoids accidental key reuse bugs
- [x] Compatibility shims are minimal and tested
- [x] No hidden global state impacting determinism

## 6. Testability and Gaps

- [x] Core functions are unit-testable without expensive runs
- [x] There is at least one fast deterministic test path
- [x] Missing tests are documented with priority

## 7. Maintainability

- [x] Docstrings describe behavior and assumptions accurately
- [x] Naming is consistent and domain-meaningful
- [x] Magic constants are either centralized or justified
- [x] Error handling is present where failures are likely

## Findings Log

Use this table during review:

| Severity | File:Line | Issue | Why it matters | Suggested fix |
|----------|-----------|-------|----------------|---------------|
| Low | `ufrf_ssb/hamiltonian.py:79` | Directed edge duplication remains backend-semantics sensitive during dependency upgrades. | Could silently change effective energy normalization if backend semantics change. | Keep `tests/test_balanced_model_construction.py` in CI and re-run on THRML/JAX upgrades. |
