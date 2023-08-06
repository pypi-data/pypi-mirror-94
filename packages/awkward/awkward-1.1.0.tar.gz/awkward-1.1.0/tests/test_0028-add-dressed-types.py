# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test_fromnumpy():
    a = np.arange(2 * 3 * 5).reshape((2, 3, 5))
    b = ak.from_numpy(a)
    assert ak.to_list(a) == ak.to_list(b)


def test_highlevel():
    a = ak.Array(
        [[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6], [7.7, 8.8, 9.9]], check_valid=True
    )
    assert (
        repr(a)
        == "<Array [[1.1, 2.2, 3.3], ... [7.7, 8.8, 9.9]] type='5 * var * float64'>"
    )
    assert str(a) == "[[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6], [7.7, 8.8, 9.9]]"

    b = ak.Array(np.arange(100, dtype=np.int32), check_valid=True)
    assert (
        repr(b) == "<Array [0, 1, 2, 3, 4, ... 95, 96, 97, 98, 99] type='100 * int32'>"
    )
    assert (
        str(b)
        == "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ... 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]"
    )

    c = ak.Array(
        '[{"one": 3.14, "two": [1.1, 2.2]}, {"one": 99.9, "two": [-3.1415926]}]',
        check_valid=True,
    )
    assert (
        repr(c)
        == '<Array [{one: 3.14, two: [1.1, ... -3.14]}] type=\'2 * {"one": float64, "two": va...\'>'
    )
    assert str(c) == "[{one: 3.14, two: [1.1, 2.2]}, {one: 99.9, two: [-3.14]}]"


class Dummy(ak.highlevel.Array):
    pass


def test_string1():
    a = ak.Array(
        np.array([ord(x) for x in "hey there"], dtype=np.uint8), check_valid=True
    )
    a.__class__ = ak.behaviors.string.ByteBehavior
    assert str(a) == str(b"hey there")
    assert repr(a) == repr(b"hey there")


def test_string2():
    content = ak.layout.NumpyArray(
        np.array([ord(x) for x in "heythere"], dtype=np.uint8)
    )
    listoffsetarray = ak.layout.ListOffsetArray64(
        ak.layout.Index64(np.array([0, 3, 3, 8])), content
    )
    a = ak.Array(listoffsetarray, check_valid=True)

    assert isinstance(a, ak.Array)
    assert not isinstance(a, ak.behaviors.string.StringBehavior)
    assert ak.to_list(a) == [[104, 101, 121], [], [116, 104, 101, 114, 101]]

    assert repr(ak.type(a)) == "3 * var * uint8"
    assert repr(ak.type(a[0])) == "3 * uint8"
    assert repr(ak.type(a[1])) == "0 * uint8"
    assert repr(ak.type(a[2])) == "5 * uint8"

    assert (
        repr(a)
        == "<Array [[104, 101, 121], ... 101, 114, 101]] type='3 * var * uint8'>"
    )
    assert str(a) == "[[104, 101, 121], [], [116, 104, 101, 114, 101]]"
    assert repr(a[0]) == "<Array [104, 101, 121] type='3 * uint8'>"
    assert repr(a[1]) == "<Array [] type='0 * uint8'>"
    assert repr(a[2]) == "<Array [116, 104, 101, 114, 101] type='5 * uint8'>"

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
