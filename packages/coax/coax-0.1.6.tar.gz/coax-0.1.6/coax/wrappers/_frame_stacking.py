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

from collections import deque

import gym


class FrameStacking(gym.Wrapper):
    r"""

    Wrapper that does frame stacking (see `DQN paper
    <https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf>`_).

    This implementation is different from most implementations in that it doesn't perform the
    stacking itself. Instead, it just returns a tuple of frames (untouched), which may be stacked
    downstream.

    The benefit of this implementation is two-fold. First, it respects the :mod:`gym.spaces` API,
    where each observation is truly an element of the observation space (this is not true of the gym
    implementation, which uses a custom data class to maintain its minimal memory footprint).
    Second, this implementation is compatibility with the :mod:`jax.tree_util` module, which means
    that we can feed it into jit-compiled functions directly.

    Example
    -------

    .. code::

        import gym
        env = gym.make('PongNoFrameskip-v0')
        print(env.observation_space)  # Box(210, 160, 3)

        env = FrameStacking(env, num_frames=2)
        print(env.observation_space)  # Tuple((Box(210, 160, 3), Box(210, 160, 3)))

    Parameters
    ----------
    env : gym-style environment

        The original environment to be wrapped.

    num_frames : positive int

        Number of frames to stack.

    """
    def __init__(self, env, num_frames):
        if not (isinstance(num_frames, int) and num_frames > 0):
            raise TypeError(f"num_frames must be a positive int, got: {num_frames}")

        super().__init__(env)
        self.observation_space = gym.spaces.Tuple((self.env.observation_space,) * num_frames)
        self._frames = deque(maxlen=num_frames)

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        self._frames.append(observation)
        return tuple(self._frames), reward, done, info

    def reset(self, **kwargs):
        observation = self.env.reset(**kwargs)
        self._frames.extend(observation for _ in range(self._frames.maxlen))
        return tuple(self._frames)  # shallow copy
