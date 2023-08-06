# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test():
    array = ak.Array([{"x": 1}])
    array["y"] = ak.virtual(lambda: [2], cache={}, length=1)
    ak.to_list(array)
