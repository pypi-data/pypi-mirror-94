// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS_C("src/cpu-kernels/awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64.cpp", line)

#include "awkward/kernels.h"

template <typename T>
ERROR awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64(
  int64_t* nextshifts,
  const T* index,
  int64_t length) {
  int64_t nullsum = 0;
  int64_t k = 0;
  for (int64_t i = 0;  i < length;  i++) {
    if (index[i] >= 0) {
      nextshifts[k] = nullsum;
      k++;
    }
    else {
      nullsum++;
    }
  }
  return success();
}
ERROR awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_64(
  int64_t* nextshifts,
  const int32_t* index,
  int64_t length) {
  return awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64<int32_t>(
    nextshifts,
    index,
    length);
}
ERROR awkward_IndexedArrayU32_reduce_next_nonlocal_nextshifts_64(
  int64_t* nextshifts,
  const uint32_t* index,
  int64_t length) {
  return awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64<uint32_t>(
    nextshifts,
    index,
    length);
}
ERROR awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64(
  int64_t* nextshifts,
  const int64_t* index,
  int64_t length) {
  return awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64<int64_t>(
    nextshifts,
    index,
    length);
}
