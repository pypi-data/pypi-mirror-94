# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test():
    one = ak.Array([999, 123, 1, 2, 3, 4, 5])
    two = ak.Array([999])[:0]
    three = ak.Array([])

    assert ak.to_list(one[[None, None]]) == [None, None]
    assert ak.to_list(one[[None, 0, None]]) == [None, 999, None]

    assert ak.to_list(two[[None, None]]) == [None, None]
    assert ak.to_list(two[[None, None, None]]) == [None, None, None]

    assert ak.to_list(three[[None, None]]) == [None, None]
    assert ak.to_list(three[[None, None, None]]) == [None, None, None]

    array = ak.Array([[[0, 1, 2], []], [[], [3, 4]], [[5], [6, 7, 8, 9]]])
    assert ak.to_list(array[:, [None, 1, None]]) == [
        [None, [], None],
        [None, [3, 4], None],
        [None, [6, 7, 8, 9], None],
    ]
    assert ak.to_list(array[:2, [None, 1, None]]) == [
        [None, [], None],
        [None, [3, 4], None],
    ]
    assert ak.to_list(array[1:, [None, 1, None]]) == [
        [None, [3, 4], None],
        [None, [6, 7, 8, 9], None],
    ]
    assert ak.to_list(array[:0, [None, 1, None]]) == []
