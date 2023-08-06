# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test():
    for itype in ["i8", "u8", "i32", "u32", "i64"]:
        form = ak.forms.ListOffsetForm(itype, ak.forms.EmptyForm())
        assert form.offsets == itype
