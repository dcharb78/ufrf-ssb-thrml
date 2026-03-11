# Master Review Checklist

Use this checklist to run a complete review from start to finish.

## Current Status (2026-03-09)

- Reproducibility track: `completed`
- Evidence: `docs/review/REPRO_VALIDATION_2026-03-09.md`
- Stochastic documentation-layer audit: `completed`
- Evidence: `docs/review/STOCHASTIC_AUDIT_5PASS_2026-03-09.md`
- Symbolic stochastic meta-audit (10-pass): `completed`
- Evidence: `docs/review/STOCHASTIC_META_AUDIT_10PASS_2026-03-09.md`
- Code-layer stochastic audit (targeted): `completed`
- Evidence: `docs/review/CODE_STOCHASTIC_AUDIT_2026-03-09.md`
- Open tracks: code correctness deep review, science/statistics deep review, final consolidated report

## 1. Preparation

- [x] Confirm Python version is 3.10+
- [x] Install dependencies from `requirements.txt` (or equivalent pinned set)
- [x] Confirm THRML version used for review
- [x] Record hardware/OS/JAX backend details in report

## 2. Reproduction

- [x] Run invariance test (`scripts/run_invariance.py`)
- [x] Run single-sector SSB test (`scripts/run_single_sector.py`)
- [x] Run two-sector mirror test (`scripts/run_two_sector.py`)
- [x] Verify output JSONL files are generated in `results/`
- [x] Compare reproduced metrics against `docs/RESULTS.md`
- [x] Record any metric drift and likely causes

## 3. Code Correctness

- [x] Review formal model equations and logic in `docs/review/MATH_AND_LOGIC_CAPTURE.md`
- [x] Validate model construction logic in `ufrf_ssb/hamiltonian.py`
- [x] Validate constants and derived quantities in `ufrf_ssb/constants.py`
- [x] Validate sampling/observables in `ufrf_ssb/sampling.py`
- [x] Validate CLI scripts for argument handling and output integrity
- [x] Verify no hidden symmetry-breaking terms in "balanced" path

## 4. Scientific Validity

- [ ] Claims match implemented experiments
- [ ] Null hypotheses are clearly stated for key tests
- [ ] Statistical tests are appropriate and correctly interpreted
- [ ] Sample sizes are justified or limitations are stated
- [ ] Confounders/alternate explanations are discussed

## 5. Reproducibility Quality

- [ ] Random seed policy is documented and deterministic where expected
- [ ] Runtime settings (warmup, samples, steps) are documented
- [ ] Output schema is stable and machine-readable
- [ ] Historical vs current results are traceable by folder/date

## 6. Review Output

- [ ] Complete `FINAL_REVIEW_REPORT_TEMPLATE.md`
- [ ] Assign overall verdict (`accept`, `accept with revisions`, `major revisions`)
- [ ] Include prioritized action list with owners and effort estimates

## 7. Stochastic Framework Audit

- [x] Run multi-pass (>=5) stochastic consistency cycles across review documents
- [x] Validate math and symmetry consistency across notation/proof/observables
- [x] Validate statistics interpretation against finite-sample uncertainty
- [x] Validate reproducibility artifacts against protocol expectations
- [x] Validate framework traceability across README/RESULTS/review docs
- [x] Record verdict and minor revisions in dedicated audit report

## 8. Symbolic Meta-Audit

- [x] Run 10-pass symbolic invariant search at document/formal-logic layer
- [x] Classify exact vs reduced vs broken vs statistical symmetries
- [x] Capture confirmed invariants vs strong inferences vs unsupported claims
- [x] Record document-level open questions and next probes
- [x] Publish dedicated audit artifact for reviewer traceability

## 9. Code Stochastic Audit

- [x] Probe bond normalization and edge multiplicities
- [x] Probe PRNG stream isolation and seed usage patterns
- [x] Probe dtype precision settings affecting energy paths
- [x] Probe magnetization/sign implementation behavior
- [x] Probe THRML schedule usage and reproducibility impact
- [x] Record prioritized findings and suggested fixes
