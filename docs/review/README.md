# Complete Review Pack

This folder contains a full markdown workflow for reviewing this repository.

## Files

1. `REVIEW_CHECKLIST.md`  
   Master checklist for a complete review run.
2. `REPRODUCTION_PROTOCOL.md`  
   Exact environment + command steps to reproduce core results.
3. `CODE_QUALITY_CHECKLIST.md`  
   Engineering and code-level review criteria.
4. `SCIENCE_AND_STATS_REVIEW.md`  
   Scientific validity and statistical rigor review criteria.
5. `FINAL_REVIEW_REPORT_TEMPLATE.md`  
   Template for final reviewer output.
6. `CHATGPT_REVIEW_PROMPT.md`  
   Copy/paste prompt for external ChatGPT review.
7. `REPRO_VALIDATION_2026-03-09.md`  
   Latest executed reproducibility validation report.
8. `MATH_AND_LOGIC_CAPTURE.md`
   Formal equations, proof logic, and claim-to-code traceability map.
9. `STOCHASTIC_AUDIT_5PASS_2026-03-09.md`
   Five-pass Monte-Carlo style consistency audit across the review framework.
10. `STOCHASTIC_META_AUDIT_10PASS_2026-03-09.md`
   Ten-pass symbolic stochastic meta-audit focused on Hamiltonian invariants at the document layer.
11. `CODE_STOCHASTIC_AUDIT_2026-03-09.md`
   Targeted code-layer stochastic audit of Hamiltonian/sampling/script correctness risks.

## Suggested Order

1. Run `REPRODUCTION_PROTOCOL.md`
2. Review `MATH_AND_LOGIC_CAPTURE.md`
3. Run stochastic framework consistency pass (`STOCHASTIC_AUDIT_5PASS_2026-03-09.md`)
4. Run symbolic meta-audit pass (`STOCHASTIC_META_AUDIT_10PASS_2026-03-09.md`)
5. Run code stochastic audit (`CODE_STOCHASTIC_AUDIT_2026-03-09.md`)
6. Complete `CODE_QUALITY_CHECKLIST.md`
7. Complete `SCIENCE_AND_STATS_REVIEW.md`
8. Consolidate findings in `FINAL_REVIEW_REPORT_TEMPLATE.md`
9. Mark final status in `REVIEW_CHECKLIST.md`

## Scope

This pack is tailored to this repo's current structure:
- `ufrf_ssb/` model and sampling implementation
- `scripts/` experiment entrypoints
- `results/` historical and reproduced outputs
- `docs/RESULTS.md` summary tables and claims

## Progress Snapshot

- Reproducibility: completed on 2026-03-09
- Stochastic review framework audit (5-pass): completed on 2026-03-09
- Symbolic stochastic meta-audit (10-pass): completed on 2026-03-09
- Code-layer stochastic audit: completed on 2026-03-09
- Code quality deep review: in progress (targeted findings captured)
- Science/statistics deep review: pending
- Final consolidated verdict: pending
