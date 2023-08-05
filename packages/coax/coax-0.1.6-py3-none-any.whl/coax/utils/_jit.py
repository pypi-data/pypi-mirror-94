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


from inspect import signature

import jax


__all__ = (
    'JittedFunc',
    'jit',
)


def jit(func, static_argnums=(), donate_argnums=()):
    r"""

    An alternative of :func:`jax.jit` that returns a picklable JIT-compiled function.

    Note that :func:`jax.jit` produces non-picklable functions, because the JIT compilation depends
    on the :code:`device` and :code:`backend`. In order to facilitate serialization, this function
    does not for the user to specify :code:`device` or :code:`backend`. Instead :func:`jax.jit` is
    called with the default: :code:`jax.jit(..., device=None, backend=None)`.

    Check out the original :func:`jax.jit` docs for a more detailed description of the arguments.

    Parameters
    ----------
    func : function

        Function to be JIT compiled.

    static_argnums : int or tuple of ints

        Arguments to exclude from JIT compilation.

    donate_argnums : int or tuple of ints

        To be donated arguments, see :func:`jax.jit`.

    Returns
    -------
    jitted_func : JittedFunc

        A picklable JIT-compiled function.

    """
    return JittedFunc(func, static_argnums, donate_argnums)


class JittedFunc:
    __slots__ = ('func', 'static_argnums', 'donate_argnums', '_jitted_func')

    def __init__(self, func, static_argnums=(), donate_argnums=()):
        self.func = func
        self.static_argnums = static_argnums
        self.donate_argnums = donate_argnums
        self._init_jitted_func()

    def __call__(self, *args, **kwargs):
        return self._jitted_func(*args, **kwargs)

    @property
    def __signature__(self):
        return signature(self.func)

    def __repr__(self):
        return self.__class__.__name__ + str(self.__signature__)

    def __getstate__(self):
        return self.func, self.static_argnums, self.donate_argnums

    def __setstate__(self, state):
        self.func, self.static_argnums, self.donate_argnums = state
        self._init_jitted_func()

    def _init_jitted_func(self):
        self._jitted_func = jax.jit(
            self.func,
            static_argnums=self.static_argnums,
            donate_argnums=self.donate_argnums)
