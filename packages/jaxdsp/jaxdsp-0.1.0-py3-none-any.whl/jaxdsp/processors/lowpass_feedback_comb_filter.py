import jax.numpy as jnp
from jax import jit, lax
from jax.ops import index_update

from jaxdsp.param import Param
from jaxdsp.processors.base import default_param_values

NAME = 'Lowpass Feedback Comb Filter'
PARAMS = [Param('feedback', 0.0), Param('damp', 0.0)]
PRESETS = {}

def init_state(buffer_size=20):
    return {
        'buffer': jnp.zeros(buffer_size),
        'buffer_index': 0,
        'filter_store': 0.0,
    }

def init_params():
    return default_param_values(PARAMS)

def default_target_params():
    return {'feedback': 0.5, 'damp': 0.5}

@jit
def tick(carry, x):
    params = carry['params']
    state = carry['state']

    out = state['buffer'][state['buffer_index']]
    state['filter_store'] = out * (1 - params['damp']) + state['filter_store'] * params['damp']

    state['buffer'] = index_update(state['buffer'], state['buffer_index'], x + state['filter_store'] * params['feedback'])
    state['buffer_index'] += 1
    state['buffer_index'] %= state['buffer'].size
    return carry, out

@jit
def tick_buffer(carry, X):
    return lax.scan(tick, carry, X)
