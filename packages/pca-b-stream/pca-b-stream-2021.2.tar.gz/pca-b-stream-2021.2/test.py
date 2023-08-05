# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import random as rndm
import sys as syst
from math import prod as Product
from typing import Any, Tuple

import numpy as nmpy
import tqdm

import pca_b_stream as pcas


N_TESTS = 1000

byte_orders = ("=", "<", ">")
elm_types = pcas.VALID_NUMPY_TYPES
enumeration_orders = ("C", "F")

dim_range = (1, 3)
length_range = (10, 100)
n_value_range = (1, 4)


def CheckEncoding(
    array: nmpy.ndarray, expected_details: Tuple[Any, ...] = None
) -> None:
    """"""
    encoding = pcas.PCA2BStream(array)
    decoding = pcas.BStream2PCA(encoding)
    assert nmpy.array_equal(array, decoding)

    if expected_details is not None:
        extracted_details = pcas.BStreamDetails(
            encoding, details="meTodl", should_print=False, should_return=True
        )
        CheckThatDetailsMatch(extracted_details, expected_details)


def CheckThatDetailsMatch(
    extracted_details: Tuple[Any, ...], expected_details: Tuple[Any, ...]
) -> None:
    """
    Details must contain: "meTodl"
    """
    for idx, (elm_1, elm_2) in enumerate(zip(extracted_details, expected_details)):
        if idx == 1:
            if elm_2 == "=":
                mismatch = ((syst.byteorder == "big") and (elm_1 == "<")) or (
                    (syst.byteorder != "big") and (elm_1 == ">")
                )
            else:
                mismatch = elm_1 != elm_2
        elif idx == 3:
            if (extracted_details[4] > 1) and (expected_details[4] > 1):
                mismatch = elm_1 != elm_2
            else:
                mismatch = False
        else:
            mismatch = elm_1 != elm_2

        if mismatch:
            assert (
                extracted_details == expected_details
            ), f"Extracted={extracted_details}; Expected={expected_details}"


def Main() -> None:
    """"""
    if syst.argv.__len__() < 2:
        n_tests = N_TESTS
    else:
        try:
            n_tests = int(syst.argv[1])
        except ValueError:
            n_tests = N_TESTS

    print("A few simple tests")

    CheckEncoding(nmpy.zeros((10, 10), dtype=nmpy.bool))
    CheckEncoding(nmpy.ones((10, 10), dtype=nmpy.bool))
    CheckEncoding(nmpy.zeros((10, 10), dtype=nmpy.uint8))
    CheckEncoding(nmpy.ones((10, 10), dtype=nmpy.uint8))
    CheckEncoding(nmpy.zeros((10, 10), dtype=nmpy.int64))
    CheckEncoding(nmpy.ones((10, 10), dtype=nmpy.int64))
    CheckEncoding(nmpy.full((10, 10), 2, dtype=nmpy.int64))
    inp_array = nmpy.empty((10, 10), dtype=nmpy.uint8)
    for row in (0, 1, 8, 9):
        for col in (0, 1, 8, 9):
            inp_array.fill(0)
            inp_array[row, col] = 1
            CheckEncoding(inp_array)

    print(f"Random tests: {n_tests}...")

    n_valid_masks = 0

    for _ in tqdm.trange(n_tests, ncols=80, mininterval=2, colour="#00aa00"):
        elm_type = rndm.choice(elm_types)
        if nmpy.dtype(elm_type).byteorder == "|":
            full_dtype = "|" + elm_type
            dtype = elm_type
        else:
            full_dtype = rndm.choice(byte_orders) + elm_type
            dtype = full_dtype
        enumeration_order = rndm.choice(enumeration_orders)

        dimension = rndm.randint(*dim_range)
        shape = tuple(rndm.randint(*length_range) for _ in range(dimension))

        inp_array = nmpy.random.random(size=Product(shape))
        n_values = rndm.randint(*n_value_range)  # Other than zero
        if n_values > 1:
            inp_array = nmpy.digitize(inp_array, nmpy.linspace(0.0, 1.0, num=n_values + 2))
        else:
            inp_array = inp_array > 0.5
        inp_array = inp_array.astype(dtype)
        inp_array = nmpy.reshape(inp_array, shape, order=enumeration_order)

        mask_is_valid, _ = pcas.PCAIsValid(inp_array)
        if not mask_is_valid:
            continue
        n_valid_masks += 1

        # nmpy.sctypeDict: see note on multiple-code types in pca_b_stream.py
        details = (
            int(nmpy.max(inp_array)),
            full_dtype[0],
            nmpy.sctypeDict[full_dtype[1]].__name__,
            enumeration_order,
            dimension,
            shape,
        )

        CheckEncoding(inp_array, expected_details=details)

    print(f"Actual tests: {n_valid_masks}/{n_tests}")


if __name__ == "__main__":
    #
    Main()
