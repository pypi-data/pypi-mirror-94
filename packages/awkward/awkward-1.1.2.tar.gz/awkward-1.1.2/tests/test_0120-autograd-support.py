# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

autograd = pytest.importorskip("autograd")


def tanh(x):
    y = np.exp(-2.0 * x)
    return (1.0 - y) / (1.0 + y)


def test_flat():
    grad_tanh = ak.autograd.elementwise_grad(tanh)

    xs = ak.Array(np.linspace(-3, 3, 10), check_valid=True)
    assert ak.to_list(xs) == pytest.approx(
        [
            -3.0,
            -2.3333333333333335,
            -1.6666666666666667,
            -1.0,
            -0.3333333333333335,
            0.33333333333333304,
            1.0,
            1.666666666666666,
            2.333333333333333,
            3.0,
        ]
    )

    assert ak.to_list(tanh(xs)) == pytest.approx(
        [
            -0.9950547536867305,
            -0.9813680813098666,
            -0.9311096086675776,
            -0.7615941559557649,
            -0.32151273753163445,
            0.32151273753163406,
            0.7615941559557649,
            0.9311096086675775,
            0.9813680813098666,
            0.9950547536867306,
        ]
    )

    assert ak.to_list(grad_tanh(xs)) == pytest.approx(
        [
            0.009866037165439843,
            0.036916688986191167,
            0.1330348966469106,
            0.4199743416140259,
            0.8966295596049142,
            0.8966295596049146,
            0.419974341614026,
            0.13303489664691054,
            0.03691668898619103,
            0.009866037165440192,
        ]
    )


def parabola(x):
    return 3 * x ** 2


def test_jagged():
    grad_parabola = ak.autograd.elementwise_grad(parabola)

    array = ak.Array([[1.0, 2.0, 3.0], [], [4.0, None, 5.0]], check_valid=True)

    assert ak.to_list(array) == [[1.0, 2.0, 3.0], [], [4.0, None, 5.0]]
    assert ak.to_list(parabola(array)) == [[3.0, 12.0, 27.0], [], [48.0, None, 75.0]]
    assert ak.to_list(grad_parabola(array)) == [
        [6.0, 12.0, 18.0],
        [],
        [24.0, None, 30.0],
    ]
