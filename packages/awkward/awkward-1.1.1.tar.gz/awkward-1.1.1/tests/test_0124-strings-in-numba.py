# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

numba = pytest.importorskip("numba")


def test_string():
    array = ak.Array(["one", "two", "three", "four", "five"], check_valid=True)

    def f1(x, i):
        return x[i]

    assert f1(array, 0) == "one"
    assert f1(array, 1) == "two"
    assert f1(array, 2) == "three"

    f1 = numba.njit(f1)

    assert f1(array, 0) == "one"
    assert f1(array, 1) == "two"
    assert f1(array, 2) == "three"

    if not ak._util.py27:

        def f2(x, i, j):
            return x[i] + x[j]

        assert f2(array, 1, 3) == "twofour"
        assert numba.njit(f2)(array, 1, 3) == "twofour"


def test_bytestring():
    array = ak.Array([b"one", b"two", b"three", b"four", b"five"], check_valid=True)

    def f1(x, i):
        return x[i]

    assert f1(array, 0) == b"one"
    assert f1(array, 1) == b"two"
    assert f1(array, 2) == b"three"

    f1 = numba.njit(f1)

    assert f1(array, 0) == b"one"
    assert f1(array, 1) == b"two"
    assert f1(array, 2) == b"three"
