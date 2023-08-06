# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test_parameters_on_arrays():
    a = ak.layout.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5]))
    assert a.parameters == {}
    a.setparameter("one", ["two", 3, {"four": 5}])
    assert a.parameters == {"one": ["two", 3, {"four": 5}]}

    b = ak.layout.ListOffsetArray64(
        ak.layout.Index64(np.array([0, 3, 3, 5], dtype=np.int64)), a
    )
    assert b.parameters == {}
    assert b.content.parameters == {"one": ["two", 3, {"four": 5}]}
    b.setparameter("what", "ever")
    assert b.parameters == {"what": "ever"}
    assert b.content.parameters == {"one": ["two", 3, {"four": 5}]}


def test_string2():
    content = ak.layout.NumpyArray(
        np.array([ord(x) for x in "heythere"], dtype=np.uint8),
        parameters={"__array__": "char", "encoding": "utf-8"},
    )
    listoffsetarray = ak.layout.ListOffsetArray64(
        ak.layout.Index64(np.array([0, 3, 3, 8])),
        content,
        parameters={"__array__": "string"},
    )
    a = ak.Array(listoffsetarray, check_valid=True)

    assert isinstance(a, ak.Array)
    assert ak.to_list(a) == ["hey", "", "there"]

    if ak._util.py27:
        assert str(a) == "[u'hey', u'', u'there']"
        assert repr(a[0]) == "u'hey'"
        assert repr(a[1]) == "u''"
        assert repr(a[2]) == "u'there'"
    else:
        assert str(a) == "['hey', '', 'there']"
        assert repr(a[0]) == "'hey'"
        assert repr(a[1]) == "''"
        assert repr(a[2]) == "'there'"


def test_dress():
    class Dummy(ak.highlevel.Array):
        def __repr__(self):
            return "<Dummy {0}>".format(str(self))

    ns = {"Dummy": Dummy}

    x = ak.layout.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5]))
    x.setparameter("__array__", "Dummy")
    a = ak.Array(x, behavior=ns, check_valid=True)
    assert repr(a) == "<Dummy [1.1, 2.2, 3.3, 4.4, 5.5]>"

    x2 = ak.layout.ListOffsetArray64(
        ak.layout.Index64(np.array([0, 3, 3, 5], dtype=np.int64)),
        ak.layout.NumpyArray(
            np.array([1.1, 2.2, 3.3, 4.4, 5.5]), parameters={"__array__": "Dummy"}
        ),
    )
    a2 = ak.Array(x2, behavior=ns, check_valid=True)
    assert (
        repr(a2)
        == "<Array [<Dummy [1.1, 2.2, 3.3]>, ... ] type='3 * var * float64[parameters={\"__ar...'>"
    )
    assert repr(a2[0]) == "<Dummy [1.1, 2.2, 3.3]>"
    assert repr(a2[1]) == "<Dummy []>"
    assert repr(a2[2]) == "<Dummy [4.4, 5.5]>"
