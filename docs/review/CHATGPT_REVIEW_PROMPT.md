# ChatGPT Review Prompt

Copy this prompt into ChatGPT along with this repository context.

```text
You are conducting a strict technical review of a Python/JAX repository that studies Z2 symmetry and spontaneous symmetry breaking using THRML.

Review goals:
1) Validate code correctness and implementation integrity.
2) Validate scientific claims against available evidence.
3) Validate statistical interpretation and reproducibility quality.

Use these files as primary review guides:
- docs/review/REVIEW_CHECKLIST.md
- docs/review/REPRODUCTION_PROTOCOL.md
- docs/review/REPRO_VALIDATION_2026-03-09.md
- docs/review/MATH_AND_LOGIC_CAPTURE.md
- docs/review/STOCHASTIC_AUDIT_5PASS_2026-03-09.md
- docs/review/STOCHASTIC_META_AUDIT_10PASS_2026-03-09.md
- docs/review/CODE_STOCHASTIC_AUDIT_2026-03-09.md
- docs/review/CODE_QUALITY_CHECKLIST.md
- docs/review/SCIENCE_AND_STATS_REVIEW.md
- docs/review/FINAL_REVIEW_REPORT_TEMPLATE.md

Repository files of interest:
- README.md
- docs/RESULTS.md
- ufrf_ssb/constants.py
- ufrf_ssb/hamiltonian.py
- ufrf_ssb/sampling.py
- scripts/run_invariance.py
- scripts/run_single_sector.py
- scripts/run_two_sector.py

Instructions:
- Be critical and specific; avoid generic advice.
- Prioritize concrete bugs, regressions, and overclaims.
- For each issue, include severity and exact file/line references.
- Separate confirmed issues from assumptions.
- Stress-test cross-document consistency using multi-pass stochastic review logic.
- Treat reproducibility as already validated and focus remaining effort on correctness, claims, and statistical interpretation.
- If evidence is insufficient, state what data or run is missing.
- End with a clear verdict: accept / accept with revisions / major revisions.
```
