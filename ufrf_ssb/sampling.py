"""
THRML-based thermodynamic relaxation for UFRF lattice models.
"""

import jax
import jax.numpy as jnp

from thrml import Block, SamplingSchedule, sample_states
from thrml.models import IsingSamplingProgram, hinton_init


def relax(model, nodes, n, seed, warmup=50, n_samples=200, steps_per=3):
    """
    Run THRML MCMC relaxation (exothermic sampling).

    Starting from a random (Hinton) initialization, the system relaxes
    toward lower-energy configurations through thermodynamic sampling.

    Args:
        model: IsingEBM model
        nodes: List of SpinNode
        n: Number of nodes
        seed: RNG seed
        warmup: Number of warmup steps (discarded)
        n_samples: Number of samples to collect
        steps_per: MCMC steps between samples

    Returns:
        Array of shape (n_samples, n) with spin states {0, 1}
    """
    block_even = Block(nodes[0::2])
    block_odd = Block(nodes[1::2])
    observe = Block(tuple(nodes))

    program = IsingSamplingProgram(
        model, free_blocks=[block_even, block_odd], clamped_blocks=[]
    )

    k1, k2 = jax.random.split(jax.random.PRNGKey(seed))
    init_state = list(hinton_init(k1, model, [block_even, block_odd], ()))

    schedule = SamplingSchedule(
        n_warmup=warmup, n_samples=n_samples, steps_per_sample=steps_per
    )

    result = sample_states(k2, program, schedule, init_state, [], [observe])
    return result[0]  # (n_samples, n)


def energy(model, nodes, spin):
    """Compute energy of a spin configuration."""
    return float(model.energy([spin], [Block(tuple(nodes))]))


def magnetization(spin):
    """Order parameter: mean of signed spins."""
    signed = spin * 2.0 - 1.0  # {0,1} -> {-1,+1}
    return float(jnp.mean(signed))


def sign_of(spin):
    """Sign of the order parameter (+1, -1, or 0)."""
    m = magnetization(spin)
    return 1.0 if m > 0 else (-1.0 if m < 0 else 0.0)
