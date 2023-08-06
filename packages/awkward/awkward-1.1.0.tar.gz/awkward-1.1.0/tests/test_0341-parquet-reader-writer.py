# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import os

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


pyarrow_parquet = pytest.importorskip("pyarrow.parquet")


def test_write_read(tmp_path):
    array1 = ak.Array([[1, 2, 3], [], [4, 5], [], [], [6, 7, 8, 9]])
    array2 = ak.repartition(array1, 2)
    array3 = ak.Array(
        [
            {"x": 1, "y": 1.1},
            {"x": 2, "y": 2.2},
            {"x": 3, "y": 3.3},
            {"x": 4, "y": 4.4},
            {"x": 5, "y": 5.5},
            {"x": 6, "y": 6.6},
            {"x": 7, "y": 7.7},
            {"x": 8, "y": 8.8},
            {"x": 9, "y": 9.9},
        ]
    )
    array4 = ak.repartition(array3, 2)

    ak.to_parquet(array1, os.path.join(tmp_path, "array1.parquet"))
    ak.to_parquet(array2, os.path.join(tmp_path, "array2.parquet"))
    ak.to_parquet(array3, os.path.join(tmp_path, "array3.parquet"))
    ak.to_parquet(array4, os.path.join(tmp_path, "array4.parquet"))

    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array1.parquet"))
    ) == ak.to_list(array1)
    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array2.parquet"))
    ) == ak.to_list(array2)
    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array3.parquet"))
    ) == ak.to_list(array3)
    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array4.parquet"))
    ) == ak.to_list(array4)

    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array1.parquet"), lazy=True)
    ) == ak.to_list(array1)
    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array2.parquet"), lazy=True)
    ) == ak.to_list(array2)
    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array3.parquet"), lazy=True)
    ) == ak.to_list(array3)
    assert ak.to_list(
        ak.from_parquet(os.path.join(tmp_path, "array4.parquet"), lazy=True)
    ) == ak.to_list(array4)


def test_explode(tmp_path):
    array3 = ak.Array(
        [
            [{"x": 1, "y": 1.1}, {"x": 2, "y": 2.2}, {"x": 3, "y": 3.3}],
            [],
            [{"x": 4, "y": 4.4}, {"x": 5, "y": 5.5}],
            [],
            [],
            [
                {"x": 6, "y": 6.6},
                {"x": 7, "y": 7.7},
                {"x": 8, "y": 8.8},
                {"x": 9, "y": 9.9},
            ],
        ]
    )
    array4 = ak.repartition(array3, 2)

    ak.to_parquet(
        array3, os.path.join(tmp_path, "array3.parquet"), explode_records=True
    )
    ak.to_parquet(
        array4, os.path.join(tmp_path, "array4.parquet"), explode_records=True
    )

    assert ak.from_parquet(os.path.join(tmp_path, "array3.parquet")).tolist() == [
        {"x": [1, 2, 3], "y": [1.1, 2.2, 3.3]},
        {"x": [], "y": []},
        {"x": [4, 5], "y": [4.4, 5.5]},
        {"x": [], "y": []},
        {"x": [], "y": []},
        {"x": [6, 7, 8, 9], "y": [6.6, 7.7, 8.8, 9.9]},
    ]
    assert ak.from_parquet(os.path.join(tmp_path, "array4.parquet")).tolist() == [
        {"x": [1, 2, 3], "y": [1.1, 2.2, 3.3]},
        {"x": [], "y": []},
        {"x": [4, 5], "y": [4.4, 5.5]},
        {"x": [], "y": []},
        {"x": [], "y": []},
        {"x": [6, 7, 8, 9], "y": [6.6, 7.7, 8.8, 9.9]},
    ]


def test_oamap_samples():
    assert ak.to_list(ak.from_parquet("tests/samples/list-depths-simple.parquet")) == [
        {"list0": 1, "list1": [1]},
        {"list0": 2, "list1": [1, 2]},
        {"list0": 3, "list1": [1, 2, 3]},
        {"list0": 4, "list1": [1, 2, 3, 4]},
        {"list0": 5, "list1": [1, 2, 3, 4, 5]},
    ]
    assert ak.to_list(
        ak.from_parquet("tests/samples/nullable-record-primitives.parquet")
    ) == [
        {
            "u1": None,
            "u4": 1,
            "u8": None,
            "f4": 1.100000023841858,
            "f8": None,
            "raw": b"one",
            "utf8": "one",
        },
        {
            "u1": 1,
            "u4": None,
            "u8": 2,
            "f4": 2.200000047683716,
            "f8": None,
            "raw": None,
            "utf8": None,
        },
        {
            "u1": None,
            "u4": None,
            "u8": 3,
            "f4": None,
            "f8": None,
            "raw": b"three",
            "utf8": None,
        },
        {
            "u1": 0,
            "u4": None,
            "u8": 4,
            "f4": None,
            "f8": 4.4,
            "raw": None,
            "utf8": None,
        },
        {
            "u1": None,
            "u4": 5,
            "u8": None,
            "f4": None,
            "f8": 5.5,
            "raw": None,
            "utf8": "five",
        },
    ]
    assert ak.to_list(
        ak.from_parquet("tests/samples/nullable-record-primitives-simple.parquet")
    ) == [
        {"u4": None, "u8": 1},
        {"u4": None, "u8": 2},
        {"u4": None, "u8": 3},
        {"u4": None, "u8": 4},
        {"u4": None, "u8": 5},
    ]
    assert ak.to_list(ak.from_parquet("tests/samples/record-primitives.parquet")) == [
        {
            "u1": 0,
            "u4": 1,
            "u8": 1,
            "f4": 1.100000023841858,
            "f8": 1.1,
            "raw": b"one",
            "utf8": "one",
        },
        {
            "u1": 1,
            "u4": 2,
            "u8": 2,
            "f4": 2.200000047683716,
            "f8": 2.2,
            "raw": b"two",
            "utf8": "two",
        },
        {
            "u1": 1,
            "u4": 3,
            "u8": 3,
            "f4": 3.299999952316284,
            "f8": 3.3,
            "raw": b"three",
            "utf8": "three",
        },
        {
            "u1": 0,
            "u4": 4,
            "u8": 4,
            "f4": 4.400000095367432,
            "f8": 4.4,
            "raw": b"four",
            "utf8": "four",
        },
        {
            "u1": 0,
            "u4": 5,
            "u8": 5,
            "f4": 5.5,
            "f8": 5.5,
            "raw": b"five",
            "utf8": "five",
        },
    ]
    assert ak.to_list(ak.from_parquet("tests/samples/nonnullable-depths.parquet")) == [
        {"whatever": {"r0": [{"r1": [{"r2": [0, 1, 2, 3]}]}]}},
        {"whatever": {"r0": [{"r1": [{"r2": []}]}]}},
        {"whatever": {"r0": [{"r1": []}]}},
        {"whatever": {"r0": []}},
        {"whatever": {"r0": []}},
        {"whatever": {"r0": [{"r1": []}]}},
        {"whatever": {"r0": [{"r1": [{"r2": []}]}]}},
        {"whatever": {"r0": [{"r1": [{"r2": [0, 1, 2, 3]}]}]}},
    ]
    assert ak.to_list(ak.from_parquet("tests/samples/nullable-depths.parquet")) == [
        {"whatever": {"r0": [{"r1": [{"r2": [0, 1, 2, 3]}]}]}},
        {"whatever": {"r0": [{"r1": [{"r2": []}]}]}},
        {"whatever": {"r0": [{"r1": []}]}},
        {"whatever": {"r0": []}},
        {"whatever": None},
        {"whatever": {"r0": []}},
        {"whatever": {"r0": [{"r1": []}]}},
        {"whatever": {"r0": [{"r1": [{"r2": []}]}]}},
        {"whatever": {"r0": [{"r1": [{"r2": [0, 1, 2, 3]}]}]}},
    ]
    assert ak.to_list(ak.from_parquet("tests/samples/nullable-levels.parquet")) == [
        {"whatever": {"r0": {"r1": {"r2": {"r3": 1}}}}},
        {"whatever": {"r0": {"r1": {"r2": {"r3": None}}}}},
        {"whatever": {"r0": {"r1": {"r2": None}}}},
        {"whatever": {"r0": None}},
        {"whatever": None},
        {"whatever": {"r0": None}},
        {"whatever": {"r0": {"r1": {"r2": None}}}},
        {"whatever": {"r0": {"r1": {"r2": {"r3": None}}}}},
        {"whatever": {"r0": {"r1": {"r2": {"r3": 1}}}}},
    ]

    # ak.to_list(ak.from_parquet("tests/samples/list-depths.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/list-depths-records-list.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/list-depths-records.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/list-depths-strings.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/list-lengths.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/nullable-list-depths.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/nullable-list-depths-records-list.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/nullable-list-depths-records.parquet"))
    # ak.to_list(ak.from_parquet("tests/samples/nullable-list-depths-strings.parquet"))
