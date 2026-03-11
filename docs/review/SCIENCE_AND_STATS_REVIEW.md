# Science and Statistics Review Checklist

Use this checklist to assess scientific validity and statistical rigor.

## 1. Claim-to-Evidence Traceability

- [ ] Each major claim in `README.md` has a direct data source
- [ ] Claims in `docs/RESULTS.md` are reproducible from result files
- [ ] No claim depends on unpublished/private intermediate data

## 2. Symmetry and Physics Logic

- [ ] Z2 invariance claim is tied to bias-free balanced Hamiltonian only
- [ ] Distinction between "balanced" and "ufrf" modes is explicit in conclusions
- [ ] If discussing SSB, differentiate individual-run order vs ensemble average
- [ ] Alternative explanations (initialization bias, sampling artifacts) are addressed

## 3. Experimental Design

- [ ] Seed count is adequate for stated confidence
- [ ] M-level choices are justified (14/144/1440)
- [ ] Warmup and sample counts are appropriate for mixing
- [ ] Two-sector test interpretation does not overstate anti-correlation

## 4. Statistical Methods

- [ ] Binomial test setup is correct for sign counts
- [ ] Confidence intervals include method and assumptions
- [ ] p-values are interpreted correctly (fail-to-reject vs prove)
- [ ] Multiple comparisons risk is acknowledged if many tests are run

## 5. Uncertainty and Robustness

- [ ] Random variability is explicitly reported
- [ ] Hardware/backend sensitivity is discussed
- [ ] Parameter sensitivity is checked or limitations stated
- [ ] Any non-reproduced metric is treated as a finding, not ignored

## 6. Data Integrity

- [ ] JSONL schemas are consistent within each experiment type
- [ ] No duplicate or corrupted lines in results files
- [ ] Derived summaries can be recomputed independently

## 7. Reporting Discipline

- [ ] Conclusions separate observed facts from interpretation
- [ ] Known limitations are explicit
- [ ] Forward-looking claims are marked as hypotheses, not results

## Statistical Audit Log

| Check | Status (Pass/Fail) | Notes | Evidence file |
|-------|--------------------|-------|---------------|
| Invariance exactness | Pass | Balanced-model flip deltas remain exactly zero in validation artifacts. | `docs/review/REPRO_VALIDATION_2026-03-09.md` |
| Sign distribution balance | Pass | `P(+1)=0.6`, `P(-1)=0.4` at `n=50`; treated as non-significant under `H0: p=0.5`. | `docs/review/STOCHASTIC_AUDIT_5PASS_2026-03-09.md` |
| Binomial interpretation | Pass | Bernoulli/binomial null model used correctly; avoids deterministic overclaims. | `docs/review/STOCHASTIC_AUDIT_5PASS_2026-03-09.md` |
| Reproduction consistency | Pass | Protocol commands and produced metrics align with reported docs. | `docs/review/REPRO_VALIDATION_2026-03-09.md` |
