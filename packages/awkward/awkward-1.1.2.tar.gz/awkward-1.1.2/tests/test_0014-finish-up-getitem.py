# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import itertools

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

content = ak.layout.NumpyArray(np.arange(2 * 3 * 5 * 7).reshape(-1, 7))
offsetsA = np.arange(0, 2 * 3 * 5 + 5, 5)
offsetsB = np.arange(0, 2 * 3 + 3, 3)
startsA, stopsA = offsetsA[:-1], offsetsA[1:]
startsB, stopsB = offsetsB[:-1], offsetsB[1:]

listoffsetarrayA64 = ak.layout.ListOffsetArray64(ak.layout.Index64(offsetsA), content)
listoffsetarrayA32 = ak.layout.ListOffsetArray32(ak.layout.Index32(offsetsA), content)
listarrayA64 = ak.layout.ListArray64(
    ak.layout.Index64(startsA), ak.layout.Index64(stopsA), content
)
listarrayA32 = ak.layout.ListArray32(
    ak.layout.Index32(startsA), ak.layout.Index32(stopsA), content
)
modelA = np.arange(2 * 3 * 5 * 7).reshape(2 * 3, 5, 7)

listoffsetarrayB64 = ak.layout.ListOffsetArray64(
    ak.layout.Index64(offsetsB), listoffsetarrayA64
)
listoffsetarrayB32 = ak.layout.ListOffsetArray32(
    ak.layout.Index32(offsetsB), listoffsetarrayA64
)
listarrayB64 = ak.layout.ListArray64(
    ak.layout.Index64(startsB), ak.layout.Index64(stopsB), listarrayA64
)
listarrayB32 = ak.layout.ListArray32(
    ak.layout.Index32(startsB), ak.layout.Index32(stopsB), listarrayA64
)
modelB = np.arange(2 * 3 * 5 * 7).reshape(2, 3, 5, 7)

listoffsetarrayB64.setidentities()
listoffsetarrayB32.setidentities()
listarrayB64.setidentities()
listarrayB32.setidentities()


def test_basic():
    assert ak.to_list(modelA) == ak.to_list(listoffsetarrayA64)
    assert ak.to_list(modelA) == ak.to_list(listoffsetarrayA32)
    assert ak.to_list(modelA) == ak.to_list(listarrayA64)
    assert ak.to_list(modelA) == ak.to_list(listarrayA32)
    assert ak.to_list(modelB) == ak.to_list(listoffsetarrayB64)
    assert ak.to_list(modelB) == ak.to_list(listoffsetarrayB32)
    assert ak.to_list(modelB) == ak.to_list(listarrayB64)
    assert ak.to_list(modelB) == ak.to_list(listarrayB32)


def test_listoffsetarrayA64():
    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations((0, 1, 4, -5), depth):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(None), slice(1, None), slice(None, -1), slice(None, None, 2)), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(1, None), slice(None, -1), 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], slice(1, None), slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA64[cuts])


def test_listoffsetarrayA32():
    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations((0, 1, 4, -5), depth):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(None), slice(1, None), slice(None, -1), slice(None, None, 2)), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(1, None), slice(None, -1), 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], slice(1, None), slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelA[cuts]) == ak.to_list(listoffsetarrayA32[cuts])


def test_listarrayA64():
    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations((0, 1, 4, -5), depth):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(None), slice(1, None), slice(None, -1), slice(None, None, 2)), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(1, None), slice(None, -1), 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA64[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], slice(1, None), slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA64[cuts])


def test_listarrayA32():
    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations((0, 1, 4, -5), depth):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(None), slice(1, None), slice(None, -1), slice(None, None, 2)), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            (slice(1, None), slice(None, -1), 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], 2, -2), depth
        ):
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA32[cuts])

    for depth in 0, 1, 2, 3:
        for cuts in itertools.permutations(
            ([2, 0, 0, 1], [1, -2, 0, -1], slice(1, None), slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelA[cuts]) == ak.to_list(listarrayA32[cuts])


def test_listoffsetarrayB64():
    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations((-2, -1, 0, 1, 1), depth):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listoffsetarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, 1, slice(1, None), slice(None, -1)), depth
        ):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listoffsetarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, [1, 0, 0, 1], [0, 1, -1, 1], slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelB[cuts]) == ak.to_list(listoffsetarrayB64[cuts])


def test_listoffsetarrayB32():
    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations((-2, -1, 0, 1, 1), depth):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listoffsetarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, 1, slice(1, None), slice(None, -1)), depth
        ):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listoffsetarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, [1, 0, 0, 1], [0, 1, -1, 1], slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelB[cuts]) == ak.to_list(listoffsetarrayB64[cuts])


def test_listarrayB64():
    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations((-2, -1, 0, 1, 1), depth):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, 1, slice(1, None), slice(None, -1)), depth
        ):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, [1, 0, 0, 1], [0, 1, -1, 1], slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelB[cuts]) == ak.to_list(listarrayB64[cuts])


def test_listarrayB32():
    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations((-2, -1, 0, 1, 1), depth):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, 1, slice(1, None), slice(None, -1)), depth
        ):
            assert ak.to_list(modelB[cuts]) == ak.to_list(listarrayB64[cuts])

    for depth in 0, 1, 2, 3, 4:
        for cuts in itertools.permutations(
            (-1, 0, [1, 0, 0, 1], [0, 1, -1, 1], slice(None, -1)), depth
        ):
            cuts = cuts
            while len(cuts) > 0 and isinstance(cuts[0], slice):
                cuts = cuts[1:]
            while len(cuts) > 0 and isinstance(cuts[-1], slice):
                cuts = cuts[:-1]
            if any(isinstance(x, slice) for x in cuts):
                continue
            assert ak.to_list(modelB[cuts]) == ak.to_list(listarrayB64[cuts])
