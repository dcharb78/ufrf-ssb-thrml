"""
Z2-symmetric Hamiltonian construction for UFRF lattice models.

Two energy modes:
  - "balanced": Simple nearest-neighbor Ising with REST-weighted couplings.
    Guaranteed Z2-symmetric (no bias terms). Used for clean SSB tests.
  - "ufrf": Full 13-cycle geometry with breathing phases, REST gain,
    multi-range couplings, and optional symmetry-breaking field.

Both modes satisfy H(s) = H(-s) when bias terms are zero.
"""

import jax
import jax.numpy as jnp
import jax.tree_util as jtree
import numpy as np

# THRML compatibility shim for newer JAX versions
if not hasattr(jax.tree, "flatten_with_path"):
    def _flatten_with_path(tree, is_leaf=None):
        return jtree.tree_flatten_with_path(tree, is_leaf=is_leaf)
    jax.tree.flatten_with_path = _flatten_with_path

from thrml import SpinNode, Block
from thrml.models import IsingEBM

from .constants import (
    PHI, TAU, ALPHA, BETA, REST_GAIN_FACTOR,
    COUPLING_RANGE, REST_POSITION, M_LEVEL_MAP,
)


def lattice_side(m_level: int) -> int:
    """Map M-level to lattice side length, raising on unknown levels."""
    try:
        return M_LEVEL_MAP[m_level]
    except KeyError as exc:
        known = ", ".join(str(k) for k in sorted(M_LEVEL_MAP))
        raise ValueError(
            f"Unsupported m_level={m_level}. Supported levels: {known}"
        ) from exc


def rest_mask(n: int) -> jnp.ndarray:
    """Boolean mask: True at REST positions (every 13th node, offset 9)."""
    return (jnp.arange(n) % 13) == REST_POSITION


def rest_weights(n: int) -> jnp.ndarray:
    """Per-node weight: 1.0 for bulk, 1+(sqrt(phi)-1) for REST nodes."""
    mask = rest_mask(n).astype(jnp.float32)
    return 1.0 + (jnp.sqrt(PHI) - 1.0) * mask


def build_balanced_model(m_level: int, kappa: float = 0.3, lam: float = 0.5):
    """
    Build a Z2-symmetric balanced energy model.

    Nearest-neighbor Ising on a 2D square lattice with periodic boundaries.
    Coupling strength is modulated by REST node proximity.
    No bias terms => exact Z2 symmetry: E(s) = E(-s).

    Args:
        m_level: UFRF hierarchy level (14, 144, 1440, ...)
        kappa: Base coupling strength
        lam: REST weighting factor

    Returns:
        (model, nodes, n_nodes, side)
    """
    side = lattice_side(m_level)
    n = side * side
    nodes = [SpinNode() for _ in range(n)]
    biases = jnp.zeros(n, dtype=jnp.float32)
    rw = np.array(rest_weights(n))

    edges, weights = [], []
    for r in range(side):
        for c in range(side):
            i = r * side + c
            for dr, dc in [(1, 0), (0, 1)]:
                j = ((r + dr) % side) * side + ((c + dc) % side)
                rest_avg = 0.5 * (rw[i] + rw[j])
                coupling = float(kappa * (1.0 + lam * (rest_avg - 1.0)))
                edges.extend([(nodes[i], nodes[j]), (nodes[j], nodes[i])])
                weights.extend([coupling, coupling])

    model = IsingEBM(
        nodes=nodes,
        edges=edges,
        biases=biases,
        weights=jnp.array(weights, dtype=jnp.float32),
        beta=jnp.array(1.0, dtype=jnp.float32),
    )
    return model, nodes, n, side


def build_balanced_model_noisy(
    m_level: int, noise_amp: float, noise_seed: int,
    kappa: float = 0.3, lam: float = 0.5,
):
    """
    Build balanced model with Gaussian noise in the bias field.
    Non-zero bias breaks Z2 symmetry, enabling phase transition studies.
    """
    side = lattice_side(m_level)
    n = side * side
    nodes = [SpinNode() for _ in range(n)]

    if noise_amp > 0:
        biases = noise_amp * jax.random.normal(
            jax.random.PRNGKey(noise_seed + 1000), (n,)
        )
    else:
        biases = jnp.zeros(n, dtype=jnp.float32)

    rw = np.array(rest_weights(n))
    edges, weights = [], []
    for r in range(side):
        for c in range(side):
            i = r * side + c
            for dr, dc in [(1, 0), (0, 1)]:
                j = ((r + dr) % side) * side + ((c + dc) % side)
                rest_avg = 0.5 * (rw[i] + rw[j])
                coupling = float(kappa * (1.0 + lam * (rest_avg - 1.0)))
                edges.extend([(nodes[i], nodes[j]), (nodes[j], nodes[i])])
                weights.extend([coupling, coupling])

    model = IsingEBM(
        nodes=nodes,
        edges=edges,
        biases=biases,
        weights=jnp.array(weights, dtype=jnp.float32),
        beta=jnp.array(1.0, dtype=jnp.float32),
    )
    return model, nodes, n, side


def build_ufrf_model(m_level: int, seed: int = 0, symmetry_break_amp: float = 0.005):
    """
    Build the full UFRF dual-trinity energy model.

    Features:
    - 13-cycle breathing phases with contraction at -1/phi
    - REST nodes at position 9 with sqrt(phi) gain
    - Multi-range couplings [1, 2, 3, 5]
    - REST-to-REST long-range connections
    - Cycle-to-cycle boundary links
    - Optional Gaussian symmetry-breaking field

    This is the complete energy function from exo2_updated.py (Nov 26, 2025).
    """
    side = lattice_side(m_level)
    n = side * side
    nodes = [SpinNode() for _ in range(n)]
    biases = jnp.zeros(n, dtype=jnp.float32)

    # Symmetry-breaking field
    key = jax.random.PRNGKey(137 + seed)
    k_sym, k_jit = jax.random.split(key)
    sb = symmetry_break_amp * jax.random.normal(k_sym, (n,))
    # Octave-alternating sign pattern
    indices = jnp.arange(n)
    octaves = indices // (13 * 13)
    sign = jnp.where(octaves % 2 == 1, -1.0, 1.0)
    sb = sb * sign + 0.0005 * jax.random.normal(k_jit, (n,))
    biases = biases + sb

    edges, weights = [], []
    for i in range(n):
        pos = i % 13
        breath_phase = (pos + 0.5) / 13.0
        breath = 1.0 + TAU * jnp.sin(2 * jnp.pi * breath_phase)
        if pos >= 6:
            breath = breath * -0.618034  # Contraction: -1/phi

        biases = biases.at[i].add(breath * TAU)

        for dist in COUPLING_RANGE:
            j = i + dist
            if j < n:
                phase_A = ALPHA * (i % 137) * 2 * jnp.pi * 2.0
                w_A = breath * (1 + TAU) * jnp.sin(phase_A)
                phase_B = ALPHA * (i % 137) * 2 * jnp.pi + jnp.pi / 2
                w_B = breath * (1 + TAU) * jnp.sin(phase_B)
                tw = (w_A + w_B) / 2.0
                edges.extend([(nodes[i], nodes[j]), (nodes[j], nodes[i])])
                weights.extend([float(tw), float(tw)])

        # REST-to-REST long-range connections
        if pos == REST_POSITION:
            rg = jnp.sqrt(PHI) * (1 + TAU) * REST_GAIN_FACTOR
            for past in range(REST_POSITION, i, 13):
                edges.extend([(nodes[i], nodes[past]), (nodes[past], nodes[i])])
                weights.extend([float(rg), float(rg)])

        # Cycle boundary links
        if pos == 0 and i >= 13:
            edges.extend([(nodes[i], nodes[i - 13]), (nodes[i - 13], nodes[i])])
            weights.extend([float(TAU), float(TAU)])

    model = IsingEBM(
        nodes=nodes,
        edges=edges,
        biases=biases,
        weights=jnp.array(weights, dtype=jnp.float32),
        beta=jnp.array(BETA, dtype=jnp.float32),
    )
    return model, nodes, n, side


def verify_z2_symmetry(model, nodes, n_tests: int = 10):
    """
    Numerically verify E(s) = E(-s) for random configurations.
    Returns max |E(s) - E(-s)| across n_tests random states.
    """
    obs = Block(tuple(nodes))
    n = len(nodes)
    max_delta = 0.0
    for i in range(n_tests):
        key = jax.random.PRNGKey(i + 999)
        state = jax.random.bernoulli(key, p=0.5, shape=(n,)).astype(jnp.float32)
        flipped = 1.0 - state
        e_orig = float(model.energy([state], [obs]))
        e_flip = float(model.energy([flipped], [obs]))
        delta = abs(e_flip - e_orig)
        max_delta = max(max_delta, delta)
    return max_delta
