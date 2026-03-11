# Math and Logic Capture for Review

This document captures the mathematical structure and logic flow of the repository for technical review.

Related stochastic coherence audit:
- `docs/review/STOCHASTIC_AUDIT_5PASS_2026-03-09.md`
- `docs/review/STOCHASTIC_META_AUDIT_10PASS_2026-03-09.md`

## 1. Notation

- Lattice side length: `L`
- Number of spins: `n = L^2`
- Binary spin state at site `i`: `x_i in {0,1}`
- Signed spin: `sigma_i = 2x_i - 1 in {-1,+1}`
- Global flip in binary encoding: `x -> 1 - x`
- Global flip in signed encoding: `sigma -> -sigma`
- Configuration vector: `x = (x_1, ..., x_n)`
- Energy: `E(x)`

## 2. Constants and Derived Quantities

Implementation source: `ufrf_ssb/constants.py`.

- `PRIMARY = 13` ([constants.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/constants.py#L15))
- `phi = (1 + sqrt(5))/2` ([constants.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/constants.py#L20))
- `tau = 1/(2*13*phi)` ([constants.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/constants.py#L23))
- `alpha = 1/(4*pi^3 + pi^2 + pi)` ([constants.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/constants.py#L26))
- REST index in 13-cycle: `REST_POSITION = 9` (10th position, 0-indexed)
- Coupling distances (UFRF mode): `[1,2,3,5]`
- M-level map:
  - `14 -> L=14`
  - `144 -> L=12`
  - `1440 -> L=38`
  - `14400 -> L=120`
  - `144000 -> L=379`

## 3. Balanced Model: Exact Form

Implementation source: `build_balanced_model()` in [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L49).

### 3.1 REST weighting

REST mask:
- `m_i = 1` if `i mod 13 == 9`, else `0`

Node weight:
- `r_i = 1 + (sqrt(phi)-1)m_i`

For each nearest-neighbor pair `(i,j)` on a 2D periodic lattice:
- `rest_avg_ij = (r_i + r_j)/2`
- `J_ij = kappa * (1 + lam*(rest_avg_ij - 1))`

Clarification:
- REST modulation alters coupling strengths only and does not introduce spin-linear terms.
- Therefore, in the balanced path, REST modulation does not break global Z2 symmetry.

Code mapping:
- mask/weights: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L38), [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L43)
- coupling formula: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L77)

### 3.2 Graph and boundary conditions

- Nearest-neighbor edges added for `(dr,dc) in {(1,0),(0,1)}`
- Periodic boundaries via modulo indexing
- Bidirectional edges are explicitly added `(i,j)` and `(j,i)`

Reviewer warning:
- Bidirectional insertion requires correct energy normalization to avoid accidental double counting.
- This is an implementation-sensitive property and must be validated against THRML energy conventions.

Code mapping:
- periodic indexing: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L76)
- explicit symmetry of edges: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L79)

### 3.3 Bias term

- Balanced model sets `b_i = 0` for all sites.
- This is the key structural condition for exact global Z2 invariance.

Code mapping:
- zero biases: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L68)

## 4. Z2 Symmetry Logic

### 4.1 Theoretical statement

For Ising energies with only pairwise terms in signed spins:
- `E(sigma) = -sum_(i,j) J_ij sigma_i sigma_j - sum_i h_i sigma_i + C`

Under global flip `sigma_i -> -sigma_i`:
- Pair terms are invariant: `(-sigma_i)(-sigma_j) = sigma_i sigma_j`
- Linear terms change sign: `h_i(-sigma_i) = -h_i sigma_i`

Therefore:
- `E(-sigma) = E(sigma)` iff all effective linear fields are zero.

### 4.2 Repository consequence

- Balanced path enforces zero biases, so invariance should hold exactly.
- Noisy balanced path injects random biases (`noise_amp > 0`) and therefore intentionally breaks exact Z2 invariance.
- UFRF path includes symmetry-breaking components in biases, so it is not an exact-Z2 test target.

Code mapping:
- noisy bias injection: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L104)
- ufrf bias additions: [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L152), [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L171)

## 5. Observable Definitions

Implementation source: `ufrf_ssb/sampling.py`.

- Signed magnetization:
  - `m(x) = (1/n) sum_i (2x_i - 1)`
- Sign observable:
  - `sign(x) = +1 if m>0, -1 if m<0, 0 if m=0`
- Flip check for a configuration `x`:
  - `delta_flip = E(1-x) - E(x)`

Code mapping:
- magnetization: [sampling.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/sampling.py#L55)
- sign: [sampling.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/sampling.py#L61)

## 6. Script Logic Capture

## 6.1 Invariance test

Source: [run_invariance.py](/Users/atom/ufrf-ssb-thrml/scripts/run_invariance.py#L32)

Algorithm:
1. For each requested M-level, build a fresh balanced model.
2. Draw random binary states.
3. Compute `delta = E(1-x)-E(x)`.
4. Record `max |delta|`.
5. Emit JSONL rows and summary.

Hard logic gate:
- Any non-zero systematic `delta` indicates symmetry break or implementation defect.

## 6.2 Single-sector SSB

Source: [run_single_sector.py](/Users/atom/ufrf-ssb-thrml/scripts/run_single_sector.py#L29)

Algorithm per seed:
1. Build balanced model.
2. Relax via THRML sampler.
3. Take final sample.
4. Record `sign`, `magnetization`, `delta_flip`.

Interpretation logic:
- Individual runs selecting `+1` or `-1` indicates broken-symmetry outcomes.
- Ensemble `P(+1)` near `0.5` supports unbiased vacuum selection.

## 6.3 Two-sector mirror test

Source: [run_two_sector.py](/Users/atom/ufrf-ssb-thrml/scripts/run_two_sector.py#L28)

Algorithm per seed:
1. Run sector A with seed `s`.
2. Run sector B with seed `s+10000`.
3. Record pair `(phi_sign, chi_sign)` and total `delta_flip`.
4. Compute anti-correlation fraction: `P(phi_sign * chi_sign < 0)`.

Interpretation logic:
- Values above `0.5` suggest tendency toward opposite vacua.
- This is probabilistic evidence, not deterministic coupling proof.

## 7. Statistical Capture for Review

## 7.1 Bernoulli model for sign counts

For single-sector runs:
- Let `K` be number of `+1` outcomes in `n` seeds.
- Under null hypothesis `H0: p = 0.5`, `K ~ Binomial(n, 0.5)`.

Review checks:
- Two-sided binomial p-value for observed `K`.
- Confidence interval for `p`.
- Whether claims use "consistent with 50/50" rather than "proves perfect balance."

## 7.2 Anti-correlation uncertainty

For two-sector runs:
- Let `A` be anti-correlated outcomes in `n` seeds.
- Estimated anti-correlation: `p_hat = A/n`.
- Assess uncertainty with binomial confidence intervals.

Review check:
- Distinguish "above 50% in this run" from "established physical law."

## 7.3 Domain-Structure Observables (Recommended Extensions)

These are not required for baseline acceptance, but are high-value probes for REST-modulated physics:

- Domain-wall density (global and class-conditioned)
- Cluster size distribution and persistence
- Relaxation time stratified by residue class (`i mod 13`)
- Class-resolved local magnetization trajectories

## 8. Claim-to-Code Trace Matrix

| Claim type | Mathematical condition | Code source | Validation artifact |
|------------|------------------------|-------------|---------------------|
| Exact Z2 invariance (balanced) | zero linear bias + pairwise terms | [hamiltonian.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/hamiltonian.py#L49) | `results/review_invariance.jsonl` |
| SSB per run | final magnetization sign in `{+1,-1}` | [sampling.py](/Users/atom/ufrf-ssb-thrml/ufrf_ssb/sampling.py#L61), [run_single_sector.py](/Users/atom/ufrf-ssb-thrml/scripts/run_single_sector.py#L60) | `results/review_single_M14.jsonl` |
| Ensemble near symmetry | `P(+1)` near 0.5 across seeds | [run_single_sector.py](/Users/atom/ufrf-ssb-thrml/scripts/run_single_sector.py#L81) | `docs/RESULTS.md` |
| Mirror anti-correlation trend | `P(phi*chi<0)` | [run_two_sector.py](/Users/atom/ufrf-ssb-thrml/scripts/run_two_sector.py#L80) | `results/review_two_M14.jsonl` |

## 9. Logical Boundaries and Caveats

- Exact invariance claim applies to the balanced model path with zero bias, not all model variants.
- Numerical "exact zero" depends on the model and backend; review should still check across environments.
- Anti-correlation percentages from finite seeds should be treated with uncertainty bounds.
- Reproducibility conclusions must include runtime stack (Python/JAX/THRML versions).

## 9.1 Symmetry Classification (Balanced Model)

| Symmetry class | Status | Notes |
|----------------|--------|-------|
| Global Z2 spin flip | Exact | Holds when linear field is zero (`b_i=0`). |
| Periodic lattice topology | Exact | Toroidal boundary construction is explicit. |
| Full translation symmetry | Reduced | REST residue classes (`i mod 13`) break full homogeneity. |
| Coupling-field rotational symmetry | Not guaranteed | Graph is square-regular; coupling field indexing is class-based. |
| Ensemble sign balance | Statistical | Expected near 50/50 over seeds, not exact for finite `n`. |
| Bidirectional bond normalization | Implementation-dependent | Must be validated against energy semantics in runtime backend. |
| Dtype/PRNG behavior | Implementation-dependent | Can affect reproducibility details, not formal model equations. |

## 9.2 Symbolic Invariant Search and Spectral Opportunities

Document-layer conclusions from the balanced model definition:

- Exact invariant:
  - Mirror class invariance `E(sigma) = E(-sigma)`.
- Topological invariant:
  - Uniform toroidal nearest-neighbor connectivity (weight heterogeneity only).
- Reduced spatial symmetry:
  - Residue-class modulation from REST mask.
- Structural reframing:
  - Weighted bond field `B_ij := J_ij` is a first-class analyzable object.

Strong inferences (not yet code-proven in this document):

- Weighted Laplacian analysis is natural: `L = D - J`.
- Domain-wall costs are plausibly position dependent under bond modulation.
- Excited-state/domain-state splitting can be nontrivial even with exact twofold vacuum degeneracy.

Not supported by docs alone:

- True quasiperiodic/quasi-crystal claim.
- Additional exact conserved quantity beyond energy + global mirror symmetry.
- Deterministic two-sector coupling mechanism.

Candidate emergent quantities for future audit:

- `Q1`: bond-energy histogram by REST class
- `Q2`: class-weighted domain-wall count
- `Q3`: cluster persistence by residue class
- `Q4`: class-resolved relaxation-time distribution

## 10. Reviewer Checklist (Math/Logic)

- [ ] Balanced-model equations in docs match implemented coupling and bias logic.
- [ ] Global-flip invariance proof assumptions are explicit and satisfied in the tested path.
- [ ] Distinction between balanced/noisy/UFRF model modes is preserved in conclusions.
- [ ] Statistical statements are calibrated to finite-sample uncertainty.
- [ ] All key claims are traceable to code and data artifacts.
