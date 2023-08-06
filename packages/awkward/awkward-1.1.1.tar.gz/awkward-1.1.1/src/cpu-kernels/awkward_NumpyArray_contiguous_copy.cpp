// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS_C("src/cpu-kernels/awkward_NumpyArray_contiguous_copy.cpp", line)

#include "awkward/kernels.h"

template <typename T>
ERROR awkward_NumpyArray_contiguous_copy(
  uint8_t* toptr,
  const uint8_t* fromptr,
  int64_t len,
  int64_t stride,
  const T* pos) {
  for (int64_t i = 0;  i < len;  i++) {
    memcpy(&toptr[i*stride], &fromptr[pos[i]], (size_t)stride);
  }
  return success();
}
ERROR awkward_NumpyArray_contiguous_copy_64(
  uint8_t* toptr,
  const uint8_t* fromptr,
  int64_t len,
  int64_t stride,
  const int64_t* pos) {
  return awkward_NumpyArray_contiguous_copy<int64_t>(
    toptr,
    fromptr,
    len,
    stride,
    pos);
}
