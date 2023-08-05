# ------------------------------------------------------------------------------------------------ #
# MIT License                                                                                      #
#                                                                                                  #
# Copyright (c) 2020, Microsoft Corporation                                                        #
#                                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software    #
# and associated documentation files (the "Software"), to deal in the Software without             #
# restriction, including without limitation the rights to use, copy, modify, merge, publish,       #
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the    #
# Software is furnished to do so, subject to the following conditions:                             #
#                                                                                                  #
# The above copyright notice and this permission notice shall be included in all copies or         #
# substantial portions of the Software.                                                            #
#                                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING    #
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND       #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,     #
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.          #
# ------------------------------------------------------------------------------------------------ #

import random
from collections import deque

import jax
import numpy as onp

from ..reward_tracing import TransitionBatch
from ._base import BaseReplayBuffer


__all__ = (
    'SimpleReplayBuffer',
)


class SimpleReplayBuffer(BaseReplayBuffer):
    r"""

    A simple ring buffer for experience replay.

    Parameters
    ----------
    capacity : positive int

        The capacity of the experience replay buffer.

    random_seed : int, optional

        To get reproducible results.

    """
    def __init__(self, capacity, random_seed=None):
        self._capacity = int(capacity)
        random.seed(random_seed)
        self._random_state = random.getstate()
        self.clear()  # sets self._storage

    @property
    def capacity(self):
        return self._capacity

    def add(self, transition_batch):
        r"""

        Add a transition to the experience replay buffer.

        Parameters
        ----------
        transition_batch : TransitionBatch

            A :class:`TransitionBatch <coax.reward_tracing.TransitionBatch>` object.

        """
        if not isinstance(transition_batch, TransitionBatch):
            raise TypeError(
                f"transition_batch must be a TransitionBatch, got: {type(transition_batch)}")

        transition_batch.idx = onp.arange(self._index, self._index + transition_batch.batch_size)
        self._index += transition_batch.batch_size
        self._storage.extend(transition_batch.to_singles())

    def sample(self, batch_size=32):
        r"""
        Get a batch of transitions to be used for bootstrapped updates.

        Parameters
        ----------
        batch_size : positive int, optional

            The desired batch size of the sample.

        Returns
        -------
        transitions : TransitionBatch

            A :class:`TransitionBatch <coax.reward_tracing.TransitionBatch>` object.

        """
        # sandwich sample in between setstate/getstate in case global random state was tampered with
        random.setstate(self._random_state)
        transitions = random.sample(self._storage, batch_size)
        self._random_state = random.getstate()
        return jax.tree_multimap(lambda *leaves: onp.concatenate(leaves, axis=0), *transitions)

    def clear(self):
        r""" Clear the experience replay buffer. """
        self._storage = deque(maxlen=self.capacity)
        self._index = 0

    def __len__(self):
        return len(self._storage)

    def __bool__(self):
        return bool(len(self))

    def __iter__(self):
        return iter(self._storage)
