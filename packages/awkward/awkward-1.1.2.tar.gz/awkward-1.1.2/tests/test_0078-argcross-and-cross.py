# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test_axis0():
    one = ak.Array([1.1, 2.2, 3.3])
    two = ak.Array([100, 200, 300, 400, 500])
    three = ak.Array(["a", "b"])

    assert ak.to_list(ak.cartesian([one], axis=0)) == [(1.1,), (2.2,), (3.3,)]
    assert ak.to_list(ak.cartesian({"x": one}, axis=0)) == [
        {"x": 1.1},
        {"x": 2.2},
        {"x": 3.3},
    ]

    assert ak.to_list(ak.cartesian([one, two], axis=0)) == [
        (1.1, 100),
        (1.1, 200),
        (1.1, 300),
        (1.1, 400),
        (1.1, 500),
        (2.2, 100),
        (2.2, 200),
        (2.2, 300),
        (2.2, 400),
        (2.2, 500),
        (3.3, 100),
        (3.3, 200),
        (3.3, 300),
        (3.3, 400),
        (3.3, 500),
    ]
    if not ak._util.py27 and not ak._util.py35:
        assert ak.to_list(ak.cartesian({"x": one, "y": two}, axis=0)) == [
            {"x": 1.1, "y": 100},
            {"x": 1.1, "y": 200},
            {"x": 1.1, "y": 300},
            {"x": 1.1, "y": 400},
            {"x": 1.1, "y": 500},
            {"x": 2.2, "y": 100},
            {"x": 2.2, "y": 200},
            {"x": 2.2, "y": 300},
            {"x": 2.2, "y": 400},
            {"x": 2.2, "y": 500},
            {"x": 3.3, "y": 100},
            {"x": 3.3, "y": 200},
            {"x": 3.3, "y": 300},
            {"x": 3.3, "y": 400},
            {"x": 3.3, "y": 500},
        ]
    assert ak.to_list(ak.cartesian([one, two, three], axis=0)) == [
        (1.1, 100, "a"),
        (1.1, 100, "b"),
        (1.1, 200, "a"),
        (1.1, 200, "b"),
        (1.1, 300, "a"),
        (1.1, 300, "b"),
        (1.1, 400, "a"),
        (1.1, 400, "b"),
        (1.1, 500, "a"),
        (1.1, 500, "b"),
        (2.2, 100, "a"),
        (2.2, 100, "b"),
        (2.2, 200, "a"),
        (2.2, 200, "b"),
        (2.2, 300, "a"),
        (2.2, 300, "b"),
        (2.2, 400, "a"),
        (2.2, 400, "b"),
        (2.2, 500, "a"),
        (2.2, 500, "b"),
        (3.3, 100, "a"),
        (3.3, 100, "b"),
        (3.3, 200, "a"),
        (3.3, 200, "b"),
        (3.3, 300, "a"),
        (3.3, 300, "b"),
        (3.3, 400, "a"),
        (3.3, 400, "b"),
        (3.3, 500, "a"),
        (3.3, 500, "b"),
    ]

    assert ak.to_list(ak.cartesian([one, two, three], axis=0, nested=[0])) == [
        [
            (1.1, 100, "a"),
            (1.1, 100, "b"),
            (1.1, 200, "a"),
            (1.1, 200, "b"),
            (1.1, 300, "a"),
        ],
        [
            (1.1, 300, "b"),
            (1.1, 400, "a"),
            (1.1, 400, "b"),
            (1.1, 500, "a"),
            (1.1, 500, "b"),
        ],
        [
            (2.2, 100, "a"),
            (2.2, 100, "b"),
            (2.2, 200, "a"),
            (2.2, 200, "b"),
            (2.2, 300, "a"),
        ],
        [
            (2.2, 300, "b"),
            (2.2, 400, "a"),
            (2.2, 400, "b"),
            (2.2, 500, "a"),
            (2.2, 500, "b"),
        ],
        [
            (3.3, 100, "a"),
            (3.3, 100, "b"),
            (3.3, 200, "a"),
            (3.3, 200, "b"),
            (3.3, 300, "a"),
        ],
        [
            (3.3, 300, "b"),
            (3.3, 400, "a"),
            (3.3, 400, "b"),
            (3.3, 500, "a"),
            (3.3, 500, "b"),
        ],
    ]
    assert ak.to_list(ak.cartesian([one, two, three], axis=0, nested=[1])) == [
        [(1.1, 100, "a"), (1.1, 100, "b")],
        [(1.1, 200, "a"), (1.1, 200, "b")],
        [(1.1, 300, "a"), (1.1, 300, "b")],
        [(1.1, 400, "a"), (1.1, 400, "b")],
        [(1.1, 500, "a"), (1.1, 500, "b")],
        [(2.2, 100, "a"), (2.2, 100, "b")],
        [(2.2, 200, "a"), (2.2, 200, "b")],
        [(2.2, 300, "a"), (2.2, 300, "b")],
        [(2.2, 400, "a"), (2.2, 400, "b")],
        [(2.2, 500, "a"), (2.2, 500, "b")],
        [(3.3, 100, "a"), (3.3, 100, "b")],
        [(3.3, 200, "a"), (3.3, 200, "b")],
        [(3.3, 300, "a"), (3.3, 300, "b")],
        [(3.3, 400, "a"), (3.3, 400, "b")],
        [(3.3, 500, "a"), (3.3, 500, "b")],
    ]
    assert ak.to_list(ak.cartesian([one, two, three], axis=0, nested=[0, 1])) == [
        [
            [(1.1, 100, "a"), (1.1, 100, "b")],
            [(1.1, 200, "a"), (1.1, 200, "b")],
            [(1.1, 300, "a"), (1.1, 300, "b")],
            [(1.1, 400, "a"), (1.1, 400, "b")],
            [(1.1, 500, "a"), (1.1, 500, "b")],
        ],
        [
            [(2.2, 100, "a"), (2.2, 100, "b")],
            [(2.2, 200, "a"), (2.2, 200, "b")],
            [(2.2, 300, "a"), (2.2, 300, "b")],
            [(2.2, 400, "a"), (2.2, 400, "b")],
            [(2.2, 500, "a"), (2.2, 500, "b")],
        ],
        [
            [(3.3, 100, "a"), (3.3, 100, "b")],
            [(3.3, 200, "a"), (3.3, 200, "b")],
            [(3.3, 300, "a"), (3.3, 300, "b")],
            [(3.3, 400, "a"), (3.3, 400, "b")],
            [(3.3, 500, "a"), (3.3, 500, "b")],
        ],
    ]

    assert ak.to_list(ak.cartesian([one, two, three], axis=0, nested=[])) == ak.to_list(
        ak.cartesian([one, two, three], axis=0, nested=False)
    )
    assert ak.to_list(ak.cartesian([one, two, three], axis=0, nested=[])) == ak.to_list(
        ak.cartesian([one, two, three], axis=0, nested=None)
    )
    assert ak.to_list(
        ak.cartesian([one, two, three], axis=0, nested=[0, 1])
    ) == ak.to_list(ak.cartesian([one, two, three], axis=0, nested=True))


def test_axis1():
    one = ak.Array([[0, 1, 2], [], [3, 4]])
    two = ak.Array([[100, 200], [300], [400, 500]])
    three = ak.Array([["a", "b"], ["c", "d"], ["e"]])

    assert ak.to_list(ak.cartesian([one])) == [[(0,), (1,), (2,)], [], [(3,), (4,)]]
    assert ak.to_list(ak.cartesian({"x": one})) == [
        [{"x": 0}, {"x": 1}, {"x": 2}],
        [],
        [{"x": 3}, {"x": 4}],
    ]

    assert ak.to_list(ak.cartesian([one, two])) == [
        [(0, 100), (0, 200), (1, 100), (1, 200), (2, 100), (2, 200)],
        [],
        [(3, 400), (3, 500), (4, 400), (4, 500)],
    ]
    if not ak._util.py27 and not ak._util.py35:
        assert ak.to_list(ak.cartesian({"x": one, "y": two})) == [
            [
                {"x": 0, "y": 100},
                {"x": 0, "y": 200},
                {"x": 1, "y": 100},
                {"x": 1, "y": 200},
                {"x": 2, "y": 100},
                {"x": 2, "y": 200},
            ],
            [],
            [
                {"x": 3, "y": 400},
                {"x": 3, "y": 500},
                {"x": 4, "y": 400},
                {"x": 4, "y": 500},
            ],
        ]

    assert ak.to_list(ak.cartesian([one, two, three])) == [
        [
            (0, 100, "a"),
            (0, 100, "b"),
            (0, 200, "a"),
            (0, 200, "b"),
            (1, 100, "a"),
            (1, 100, "b"),
            (1, 200, "a"),
            (1, 200, "b"),
            (2, 100, "a"),
            (2, 100, "b"),
            (2, 200, "a"),
            (2, 200, "b"),
        ],
        [],
        [(3, 400, "e"), (3, 500, "e"), (4, 400, "e"), (4, 500, "e")],
    ]

    assert ak.to_list(ak.cartesian([one, two, three], nested=[0])) == [
        [
            [(0, 100, "a"), (0, 100, "b"), (0, 200, "a"), (0, 200, "b")],
            [(1, 100, "a"), (1, 100, "b"), (1, 200, "a"), (1, 200, "b")],
            [(2, 100, "a"), (2, 100, "b"), (2, 200, "a"), (2, 200, "b")],
        ],
        [],
        [[(3, 400, "e"), (3, 500, "e")], [(4, 400, "e"), (4, 500, "e")]],
    ]
    assert ak.to_list(ak.cartesian([one, two, three], nested=[1])) == [
        [
            [(0, 100, "a"), (0, 100, "b")],
            [(0, 200, "a"), (0, 200, "b")],
            [(1, 100, "a"), (1, 100, "b")],
            [(1, 200, "a"), (1, 200, "b")],
            [(2, 100, "a"), (2, 100, "b")],
            [(2, 200, "a"), (2, 200, "b")],
        ],
        [],
        [[(3, 400, "e")], [(3, 500, "e")], [(4, 400, "e")], [(4, 500, "e")]],
    ]
    assert ak.to_list(ak.cartesian([one, two, three], nested=[0, 1])) == [
        [
            [[(0, 100, "a"), (0, 100, "b")], [(0, 200, "a"), (0, 200, "b")]],
            [[(1, 100, "a"), (1, 100, "b")], [(1, 200, "a"), (1, 200, "b")]],
            [[(2, 100, "a"), (2, 100, "b")], [(2, 200, "a"), (2, 200, "b")]],
        ],
        [],
        [[[(3, 400, "e")], [(3, 500, "e")]], [[(4, 400, "e")], [(4, 500, "e")]]],
    ]

    assert ak.to_list(ak.cartesian([one, two, three], nested=[])) == ak.to_list(
        ak.cartesian([one, two, three], nested=False)
    )
    assert ak.to_list(ak.cartesian([one, two, three], nested=[])) == ak.to_list(
        ak.cartesian([one, two, three], nested=None)
    )
    assert ak.to_list(ak.cartesian([one, two, three], nested=[0, 1])) == ak.to_list(
        ak.cartesian([one, two, three], nested=True)
    )


def test_axis2():
    one = ak.Array([[[0, 1, 2], [], [3, 4]], [[0, 1, 2], [], [3, 4]]])
    two = ak.Array([[[100, 200], [300], [400, 500]], [[100, 200], [300], [400, 500]]])

    assert ak.to_list(ak.cartesian([one, two], axis=2)) == [
        [
            [(0, 100), (0, 200), (1, 100), (1, 200), (2, 100), (2, 200)],
            [],
            [(3, 400), (3, 500), (4, 400), (4, 500)],
        ],
        [
            [(0, 100), (0, 200), (1, 100), (1, 200), (2, 100), (2, 200)],
            [],
            [(3, 400), (3, 500), (4, 400), (4, 500)],
        ],
    ]


def test_localindex():
    array = ak.from_iter(
        [[0.0, 1.1, 2.2], [], [3.3, 4.4], [5.5], [6.6, 7.7, 8.8, 9.9]], highlevel=False
    )
    assert ak.to_list(array.localindex(0)) == [0, 1, 2, 3, 4]
    assert ak.to_list(array.localindex(1)) == [[0, 1, 2], [], [0, 1], [0], [0, 1, 2, 3]]

    array = ak.from_iter(
        [[[0.0, 1.1, 2.2], [], [3.3, 4.4]], [], [[5.5]], [[6.6, 7.7, 8.8, 9.9]]],
        highlevel=False,
    )
    assert ak.to_list(array.localindex(0)) == [0, 1, 2, 3]
    assert ak.to_list(array.localindex(1)) == [[0, 1, 2], [], [0], [0]]
    assert ak.to_list(array.localindex(2)) == [
        [[0, 1, 2], [], [0, 1]],
        [],
        [[0]],
        [[0, 1, 2, 3]],
    ]

    array = ak.from_numpy(
        np.arange(2 * 3 * 5).reshape(2, 3, 5), regulararray=True, highlevel=False
    )
    assert ak.to_list(array.localindex(0)) == [0, 1]
    assert ak.to_list(array.localindex(1)) == [[0, 1, 2], [0, 1, 2]]
    assert ak.to_list(array.localindex(2)) == [
        [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]],
        [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]],
    ]


def test_argcartesian():
    one = ak.Array([[0.0, 1.1, 2.2], [], [3.3, 4.4]])
    two = ak.Array([[100, 200], [300], [400, 500]])

    assert ak.to_list(ak.argcartesian([one, two])) == [
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
        [],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ]
    if not ak._util.py27 and not ak._util.py35:
        assert ak.to_list(ak.argcartesian({"x": one, "y": two})) == [
            [
                {"x": 0, "y": 0},
                {"x": 0, "y": 1},
                {"x": 1, "y": 0},
                {"x": 1, "y": 1},
                {"x": 2, "y": 0},
                {"x": 2, "y": 1},
            ],
            [],
            [{"x": 0, "y": 0}, {"x": 0, "y": 1}, {"x": 1, "y": 0}, {"x": 1, "y": 1}],
        ]
