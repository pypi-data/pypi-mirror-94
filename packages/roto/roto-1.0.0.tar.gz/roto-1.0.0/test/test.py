import unittest

import numpy as np

from roto import RotoSolver


class _Helper:

    def __init__(self, n_param=3):
        self.kwargs_log = []
        self.args_log = []
        self.n_param = n_param

    def __call__(self, *args, **kwargs):
        self.kwargs_log.append(kwargs)
        self.args_log.append(args)
        return np.sum(args[0]).ravel()


class TestRotoSolver(unittest.TestCase):

    def test_the_function_has_been_correctly_called_in_normal_setup(self):
        func = _Helper(n_param=3)
        roto = RotoSolver(reset_to_zero=False, update_sequentially=True)
        var = np.arange(3).astype(float)
        kwargs = {'a': 1, 'b': 2}

        roto.run_one_iteration(func=func, var=var, extra_kwargs=kwargs)
        self.assertTrue(all(k == kwargs for k in func.kwargs_log))

        should_be = [
            np.array([-1.57079633, 1., 2.]),
            np.array([-1.57079633, -0.57079633, 0.42920367]),
            np.array([1.57079633, 1., 2.]),
            np.array([-1.57079633, -0.57079633, 2.]),
            np.array([-1.57079633, -0.57079633, 0.42920367]),
            np.array([-1.57079633, 2.57079633, 2.]),
            np.array([-1.57079633, -0.57079633, 0.42920367]),
            np.array([-1.57079633, -0.57079633, 0.42920367]),
            np.array([-1.57079633, -0.57079633, 3.57079633])
        ]

        self.assertTrue(all(len(item) == 1 for item in func.args_log))
        self.assertTrue(all(np.allclose(should_be[i], item[0]) for i, item in enumerate(func.args_log)))

    def test_the_function_has_been_correctly_called_with_modified_param(self):
        func = _Helper(n_param=3)
        np.random.seed(1)  # seed it such that when not update_sequentially, the behaviour is predictable.
        roto = RotoSolver(reset_to_zero=True, update_sequentially=False)
        var = np.arange(3).astype(float)
        kwargs = {'a': 1, 'b': 2}

        roto.run_one_iteration(func=func, var=var, extra_kwargs=kwargs)
        self.assertTrue(all(k == kwargs for k in func.kwargs_log))

        should_be = [
            np.array([-1.57079633, 1., 2.]),
            np.array([-1.57079633, -1.57079633, -1.57079633]),
            np.array([1.57079633, 1., 2.]),
            np.array([-1.57079633, 1., -1.57079633]),
            np.array([-1.57079633, -1.57079633, -1.57079633]),
            np.array([-1.57079633, 1., 1.57079633]),
            np.array([-1.57079633, -1.57079633, -1.57079633]),
            np.array([-1.57079633, -1.57079633, -1.57079633]),
            np.array([-1.57079633, 1.57079633, -1.57079633])
        ]

        self.assertTrue(all(len(item) == 1 for item in func.args_log))
        self.assertTrue(all(np.allclose(should_be[i], item[0]) for i, item in enumerate(func.args_log)))

    def test_suc_minimised(self):
        np.random.seed(10)
        size = 20
        a, b, c, k = [np.random.rand(size) for _ in range(4)]

        def func(var):
            return np.sum(a * np.sin(k * var + b) + c)

        x0 = np.random.rand(20)

        # print('\nrestart with x optimum\n')
        var = RotoSolver().minimise(func, x0, max_iteration=100)
        should_be = np.array([-3.53773183, -1.89732622, -3.63690614, -3.80366784,
                              -51.23571681, -5.61285752, -27.48999318, -6.82228484,
                              -6.71624979, -2.8066041, -59.46112552, -4.87190125,
                              -7.87308239, -2.96945596, -4.79650454, -43.42485359,
                              -1.91470807, -3.14380248, -1.84227176, -5.26236014])
        self.assertTrue(np.allclose(var, should_be))
        self.assertTrue(np.allclose(func(var), 0.1675518937516567))
