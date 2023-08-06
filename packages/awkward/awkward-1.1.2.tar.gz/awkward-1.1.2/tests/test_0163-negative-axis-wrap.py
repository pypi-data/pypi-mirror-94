# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test_array_3d():
    array = ak.Array(np.arange(3 * 5 * 2).reshape(3, 5, 2))
    assert ak.to_list(array) == [
        [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]],
        [[10, 11], [12, 13], [14, 15], [16, 17], [18, 19]],
        [[20, 21], [22, 23], [24, 25], [26, 27], [28, 29]],
    ]
    assert ak.num(array, axis=0) == 3
    assert ak.to_list(ak.num(array, axis=1)) == [5, 5, 5]
    assert ak.to_list(ak.num(array, axis=2)) == [
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
    ]
    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=3)
    assert str(err.value).startswith("'axis' out of range for 'num'")

    assert ak.to_list(ak.num(array, axis=-1)) == [
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
    ]
    assert ak.to_list(ak.num(array, axis=-2)) == [5, 5, 5]
    assert ak.num(array, axis=-3) == 3

    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=-4)
    assert str(err.value).startswith("axis == -4 exceeds the depth == 3 of this array")


def test_list_array():
    array = ak.Array(np.arange(3 * 5 * 2).reshape(3, 5, 2).tolist())
    assert ak.num(array, axis=0) == 3
    assert ak.num(array, axis=1).tolist() == [5, 5, 5]
    assert ak.num(array, axis=2).tolist() == [
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
    ]

    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=3)
    assert str(err.value).startswith("'axis' out of range for 'num'")

    assert ak.num(array, axis=-1).tolist() == [
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
    ]
    assert ak.num(array, axis=-2).tolist() == [5, 5, 5]
    assert ak.num(array, axis=-3) == 3
    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=-4)
    assert str(err.value).startswith("axis == -4 exceeds the depth == 3 of this array")


def test_record_array():
    array = ak.Array(
        [
            {"x": [1], "y": [[], [1]]},
            {"x": [1, 2], "y": [[], [1], [1, 2]]},
            {"x": [1, 2, 3], "y": [[], [1], [1, 2], [1, 2, 3]]},
        ]
    )

    assert ak.num(array, axis=0).tolist() == {"x": 3, "y": 3}
    assert ak.num(array, axis=1).tolist() == [
        {"x": 1, "y": 2},
        {"x": 2, "y": 3},
        {"x": 3, "y": 4},
    ]
    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=2)
    assert str(err.value).startswith("'axis' out of range for 'num'")

    assert ak.num(array, axis=-1).tolist() == [
        {"x": 1, "y": [0, 1]},
        {"x": 2, "y": [0, 1, 2]},
        {"x": 3, "y": [0, 1, 2, 3]},
    ]


def test_record_array_axis_out_of_range():
    array = ak.Array(
        [
            {"x": [1], "y": [[], [1]]},
            {"x": [1, 2], "y": [[], [1], [1, 2]]},
            {"x": [1, 2, 3], "y": [[], [1], [1, 2], [1, 2, 3]]},
        ]
    )

    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=-2)
    assert str(err.value).startswith(
        "axis == -2 exceeds the min depth == 2 of this array"
    )

    with pytest.raises(ValueError) as err:
        assert ak.num(array, axis=-3)
    assert str(err.value).startswith("axis == -3 exceeds the depth == 2 of this array")
