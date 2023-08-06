// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#include <limits>

#include "awkward/kernels.h"

#include "awkward/Reducer.h"

namespace awkward {
  util::dtype
  Reducer::return_dtype(util::dtype given_dtype) const {
    return given_dtype;
  }

  bool
  Reducer::returns_positions() const {
    return false;
  }

  ////////// count

  const std::string
  ReducerCount::name() const {
    return "count";
  }

  util::dtype
  ReducerCount::preferred_dtype() const {
    return util::dtype::float64;
  }

  util::dtype
  ReducerCount::return_dtype(util::dtype given_dtype) const {
    return util::dtype::int64;
  }

  const std::shared_ptr<void>
  ReducerCount::apply_bool(const bool* data,
                           const Index64& parents,
                           int64_t outlength) const {
    // This is the only reducer that completely ignores the data.
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_count_64(
      ptr_lib,
      ptr.get(),
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCount::apply_int8(const int8_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_uint8(const uint8_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_int16(const int16_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_uint16(const uint16_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_int32(const int32_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_uint32(const uint32_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_int64(const int64_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_uint64(const uint64_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_float32(const float* data,
                              const Index64& parents,
                              int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_float64(const double* data,
                              const Index64& parents,
                              int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_complex64(const std::complex<float>* data,
                                const Index64& parents,
                                int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  const std::shared_ptr<void>
  ReducerCount::apply_complex128(const std::complex<double>* data,
                                 const Index64& parents,
                                 int64_t outlength) const {
    return apply_bool(reinterpret_cast<const bool*>(data),
                      parents,
                      outlength);
  }

  ////////// count nonzero

  const std::string
  ReducerCountNonzero::name() const {
    return "count_nonzero";
  }

  util::dtype
  ReducerCountNonzero::preferred_dtype() const {
    return util::dtype::float64;
  }

  util::dtype
  ReducerCountNonzero::return_dtype(util::dtype given_dtype) const {
    return util::dtype::int64;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_bool(const bool* data,
                                  const Index64& parents,
                                  int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_int8(const int8_t* data,
                                  const Index64& parents,
                                  int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_uint8(const uint8_t* data,
                                   const Index64& parents,
                                   int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_int16(const int16_t* data,
                                   const Index64& parents,
                                   int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_uint16(const uint16_t* data,
                                    const Index64& parents,
                                    int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_int32(const int32_t* data,
                                   const Index64& parents,
                                   int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_uint32(const uint32_t* data,
                                    const Index64& parents,
                                    int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_int64(const int64_t* data,
                                   const Index64& parents,
                                   int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_uint64(const uint64_t* data,
                                    const Index64& parents,
                                    int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_float32(const float* data,
                                     const Index64& parents,
                                     int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_float64(const double* data,
                                     const Index64& parents,
                                     int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_complex64(const std::complex<float>* data,
                                       const Index64& parents,
                                       int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerCountNonzero::apply_complex128(const std::complex<double>* data,
                                        const Index64& parents,
                                        int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_countnonzero_64<std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// sum (addition)

  const std::string
  ReducerSum::name() const {
    return "sum";
  }

  util::dtype
  ReducerSum::preferred_dtype() const {
    return util::dtype::float64;
  }

  util::dtype
  ReducerSum::return_dtype(util::dtype given_dtype) const {
    switch (given_dtype) {
    case util::dtype::boolean:
    case util::dtype::int8:
    case util::dtype::int16:
    case util::dtype::int32:
#if defined _MSC_VER || defined __i386__
      return util::dtype::int32;
#endif
    case util::dtype::int64:
      return util::dtype::int64;
    case util::dtype::uint8:
    case util::dtype::uint16:
    case util::dtype::uint32:
#if defined _MSC_VER || defined __i386__
      return util::dtype::uint32;
#endif
    case util::dtype::uint64:
      return util::dtype::uint64;
    default:
      return given_dtype;
    }
  }

  const std::shared_ptr<void>
  ReducerSum::apply_bool(const bool* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_sum_64<int32_t, bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_sum_64<int64_t, bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_int8(const int8_t* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_sum_64<int32_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_sum_64<int64_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_uint8(const uint8_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    struct Error err = kernel::reduce_sum_64<uint32_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_sum_64<uint64_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_int16(const int16_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_sum_64<int32_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_sum_64<int64_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_uint16(const uint16_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    struct Error err = kernel::reduce_sum_64<uint32_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_sum_64<uint64_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_int32(const int32_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_sum_64<int32_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_sum_64<int64_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_uint32(const uint32_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    struct Error err = kernel::reduce_sum_64<uint32_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_sum_64<uint64_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_int64(const int64_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_sum_64<int64_t, int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_uint64(const uint64_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_sum_64<uint64_t, uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_float32(const float* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<float> ptr = kernel::malloc<float>(
      ptr_lib, outlength*(int64_t)sizeof(float));
    struct Error err = kernel::reduce_sum_64<float, float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_float64(const double* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<double> ptr = kernel::malloc<double>(
      ptr_lib, outlength*(int64_t)sizeof(double));
    struct Error err = kernel::reduce_sum_64<double, double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_complex64(const std::complex<float>* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<float>> ptr = kernel::malloc<std::complex<float>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<float>));
    struct Error err = kernel::reduce_sum_64<std::complex<float>, std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerSum::apply_complex128(const std::complex<double>* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<double>> ptr = kernel::malloc<std::complex<double>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<double>));
    struct Error err = kernel::reduce_sum_64<std::complex<double>, std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// prod (multiplication)

  const std::string
  ReducerProd::name() const {
    return "prod";
  }

  util::dtype
  ReducerProd::preferred_dtype() const {
    return util::dtype::int64;
  }

  util::dtype
  ReducerProd::return_dtype(util::dtype given_dtype) const {
    switch (given_dtype) {
    case util::dtype::boolean:
    case util::dtype::int8:
    case util::dtype::int16:
    case util::dtype::int32:
#if defined _MSC_VER || defined __i386__
      return util::dtype::int32;
#endif
    case util::dtype::int64:
      return util::dtype::int64;
    case util::dtype::uint8:
    case util::dtype::uint16:
    case util::dtype::uint32:
#if defined _MSC_VER || defined __i386__
      return util::dtype::uint32;
#endif
    case util::dtype::uint64:
      return util::dtype::uint64;
    default:
      return given_dtype;
    }
  }

  const std::shared_ptr<void>
  ReducerProd::apply_bool(const bool* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_prod_64<int32_t, bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_prod_64<int64_t, bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_int8(const int8_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*sizeof(int32_t));
    struct Error err = kernel::reduce_prod_64<int32_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_prod_64<int64_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_uint8(const uint8_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    struct Error err = kernel::reduce_prod_64<uint32_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_prod_64<uint64_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_int16(const int16_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_prod_64<int32_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_prod_64<int64_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_uint16(const uint16_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    struct Error err = kernel::reduce_prod_64<uint32_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_prod_64<uint64_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_int32(const int32_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    struct Error err = kernel::reduce_prod_64<int32_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_prod_64<int64_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_uint32(const uint32_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
#if defined _MSC_VER || defined __i386__
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    struct Error err = kernel::reduce_prod_64<uint32_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#else
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_prod_64<uint64_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
#endif
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_int64(const int64_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_prod_64<int64_t, int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_uint64(const uint64_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    struct Error err = kernel::reduce_prod_64<uint64_t, uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_float32(const float* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<float> ptr = kernel::malloc<float>(
      ptr_lib, outlength*(int64_t)sizeof(float));
    struct Error err = kernel::reduce_prod_64<float, float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_float64(const double* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<double> ptr = kernel::malloc<double>(
      ptr_lib, outlength*(int64_t)sizeof(double));
    struct Error err = kernel::reduce_prod_64<double, double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_complex64(const std::complex<float>* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<float>> ptr = kernel::malloc<std::complex<float>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<float>));
    struct Error err = kernel::reduce_prod_64<std::complex<float>, std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerProd::apply_complex128(const std::complex<double>* data,
                                const Index64& parents,
                                int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<double>> ptr = kernel::malloc<std::complex<double>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<double>));
    struct Error err = kernel::reduce_prod_64<std::complex<double>, std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// any (logical or)

  const std::string
  ReducerAny::name() const {
    return "any";
  }

  util::dtype
  ReducerAny::preferred_dtype() const {
    return util::dtype::boolean;
  }

  util::dtype
  ReducerAny::return_dtype(util::dtype given_dtype) const {
    return util::dtype::boolean;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_bool(const bool* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_int8(const int8_t* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_uint8(const uint8_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_int16(const int16_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_uint16(const uint16_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_int32(const int32_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_uint32(const uint32_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_int64(const int64_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_uint64(const uint64_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_float32(const float* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_float64(const double* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_complex64(const std::complex<float>* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAny::apply_complex128(const std::complex<double>* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// all (logical and)

  const std::string
  ReducerAll::name() const {
    return "all";
  }

  util::dtype
  ReducerAll::preferred_dtype() const {
    return util::dtype::boolean;
  }

  util::dtype
  ReducerAll::return_dtype(util::dtype given_dtype) const {
    return util::dtype::boolean;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_bool(const bool* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_int8(const int8_t* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_uint8(const uint8_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_int16(const int16_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_uint16(const uint16_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_int32(const int32_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_uint32(const uint32_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_int64(const int64_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_uint64(const uint64_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_float32(const float* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_float64(const double* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_complex64(const std::complex<float>* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerAll::apply_complex128(const std::complex<double>* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// min (minimum, in which infinity is the identity)

  ReducerMin::ReducerMin(double initial_f64,
                         uint64_t initial_u64,
                         int64_t initial_i64)
    : initial_f64_(initial_f64)
    , initial_u64_(initial_u64)
    , initial_i64_(initial_i64)
    , has_initial_(true) { }

  ReducerMin::ReducerMin()
    : initial_f64_(0.0)
    , initial_u64_((uint64_t)0)
    , initial_i64_((int64_t)0)
    , has_initial_(false) { }

  const std::string
  ReducerMin::name() const {
    return "min";
  }

  util::dtype
  ReducerMin::preferred_dtype() const {
    return util::dtype::float64;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_bool(const bool* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_prod_bool_64<bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_int8(const int8_t* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int8_t> ptr = kernel::malloc<int8_t>(
      ptr_lib, outlength*(int64_t)sizeof(int8_t));
    int8_t initial = std::numeric_limits<int8_t>::max();
    if (has_initial_) {
      initial = (int8_t)initial_i64_;
    }
    struct Error err = kernel::reduce_min_64<int8_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_uint8(const uint8_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint8_t> ptr = kernel::malloc<uint8_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint8_t));
    uint8_t initial = std::numeric_limits<uint8_t>::max();
    if (has_initial_) {
      initial = (uint8_t)initial_u64_;
    }
    struct Error err = kernel::reduce_min_64<uint8_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_int16(const int16_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int16_t> ptr = kernel::malloc<int16_t>(
      ptr_lib, outlength*(int64_t)sizeof(int16_t));
    int16_t initial = std::numeric_limits<int16_t>::max();
    if (has_initial_) {
      initial = (int16_t)initial_i64_;
    }
    struct Error err = kernel::reduce_min_64<int16_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_uint16(const uint16_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint16_t> ptr = kernel::malloc<uint16_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint16_t));
    uint16_t initial = std::numeric_limits<uint16_t>::max();
    if (has_initial_) {
      initial = (uint16_t)initial_u64_;
    }
    struct Error err = kernel::reduce_min_64<uint16_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_int32(const int32_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    int32_t initial = std::numeric_limits<int32_t>::max();
    if (has_initial_) {
      initial = (int32_t)initial_i64_;
    }
    struct Error err = kernel::reduce_min_64<int32_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_uint32(const uint32_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    uint32_t initial = std::numeric_limits<uint32_t>::max();
    if (has_initial_) {
      initial = (uint32_t)initial_u64_;
    }
    struct Error err = kernel::reduce_min_64<uint32_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_int64(const int64_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    int64_t initial = std::numeric_limits<int64_t>::max();
    if (has_initial_) {
      initial = (int64_t)initial_i64_;
    }
    struct Error err = kernel::reduce_min_64<int64_t, int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_uint64(const uint64_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    uint64_t initial = std::numeric_limits<uint64_t>::max();
    if (has_initial_) {
      initial = (uint64_t)initial_u64_;
    }
    struct Error err = kernel::reduce_min_64<uint64_t, uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_float32(const float* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<float> ptr = kernel::malloc<float>(
      ptr_lib, outlength*(int64_t)sizeof(float));
    float initial = std::numeric_limits<float>::infinity();
    if (has_initial_) {
      initial = (float)initial_f64_;
    }
    struct Error err = kernel::reduce_min_64<float, float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_float64(const double* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<double> ptr = kernel::malloc<double>(
      ptr_lib, outlength*(int64_t)sizeof(double));
    double initial = std::numeric_limits<double>::infinity();
    if (has_initial_) {
      initial = (double)initial_f64_;
    }
    struct Error err = kernel::reduce_min_64<double, double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_complex64(const std::complex<float>* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<float>> ptr = kernel::malloc<std::complex<float>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<float>));
    float initial = std::numeric_limits<float>::infinity();
    if (has_initial_) {
      initial = (float)initial_f64_;
    }
    struct Error err = kernel::reduce_min_64<std::complex<float>, std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMin::apply_complex128(const std::complex<double>* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<double>> ptr = kernel::malloc<std::complex<double>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<double>));
    double initial = std::numeric_limits<double>::infinity();
    if (has_initial_) {
      initial = (double)initial_f64_;
    }
    struct Error err = kernel::reduce_min_64<std::complex<double>, std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// max (maximum, in which -infinity is the identity)

  ReducerMax::ReducerMax(double initial_f64,
                         uint64_t initial_u64,
                         int64_t initial_i64)
    : initial_f64_(initial_f64)
    , initial_u64_(initial_u64)
    , initial_i64_(initial_i64)
    , has_initial_(true) { }

  ReducerMax::ReducerMax()
    : initial_f64_(0.0)
    , initial_u64_((uint64_t)0)
    , initial_i64_((int64_t)0)
    , has_initial_(false) { }

  const std::string
  ReducerMax::name() const {
    return "max";
  }

  util::dtype
  ReducerMax::preferred_dtype() const {
    return util::dtype::float64;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_bool(const bool* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<bool> ptr = kernel::malloc<bool>(
      ptr_lib, outlength*(int64_t)sizeof(bool));
    struct Error err = kernel::reduce_sum_bool_64<bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_int8(const int8_t* data,
                         const Index64& parents,
                         int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int8_t> ptr = kernel::malloc<int8_t>(
      ptr_lib, outlength*(int64_t)sizeof(int8_t));
    int8_t initial = std::numeric_limits<int8_t>::min();
    if (has_initial_) {
      initial = (int8_t)initial_i64_;
    }
    struct Error err = kernel::reduce_max_64<int8_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_uint8(const uint8_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint8_t> ptr = kernel::malloc<uint8_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint8_t));
    uint8_t initial = std::numeric_limits<uint8_t>::min();
    if (has_initial_) {
      initial = (uint8_t)initial_u64_;
    }
    struct Error err = kernel::reduce_max_64<uint8_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_int16(const int16_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int16_t> ptr = kernel::malloc<int16_t>(
      ptr_lib, outlength*(int64_t)sizeof(int16_t));
    int16_t initial = std::numeric_limits<int16_t>::min();
    if (has_initial_) {
      initial = (int16_t)initial_i64_;
    }
    struct Error err = kernel::reduce_max_64<int16_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_uint16(const uint16_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint16_t> ptr = kernel::malloc<uint16_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint16_t));
    uint16_t initial = std::numeric_limits<uint16_t>::min();
    if (has_initial_) {
      initial = (uint16_t)initial_u64_;
    }
    struct Error err = kernel::reduce_max_64<uint16_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_int32(const int32_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int32_t> ptr = kernel::malloc<int32_t>(
      ptr_lib, outlength*(int64_t)sizeof(int32_t));
    int32_t initial = std::numeric_limits<int32_t>::min();
    if (has_initial_) {
      initial = (int32_t)initial_i64_;
    }
    struct Error err = kernel::reduce_max_64<int32_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_uint32(const uint32_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint32_t> ptr = kernel::malloc<uint32_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint32_t));
    uint32_t initial = std::numeric_limits<uint32_t>::min();
    if (has_initial_) {
      initial = (uint32_t)initial_u64_;
    }
    struct Error err = kernel::reduce_max_64<uint32_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_int64(const int64_t* data,
                          const Index64& parents,
                          int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    int64_t initial = std::numeric_limits<int64_t>::min();
    if (has_initial_) {
      initial = (int64_t)initial_i64_;
    }
    struct Error err = kernel::reduce_max_64<int64_t, int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_uint64(const uint64_t* data,
                           const Index64& parents,
                           int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<uint64_t> ptr = kernel::malloc<uint64_t>(
      ptr_lib, outlength*(int64_t)sizeof(uint64_t));
    uint64_t initial = std::numeric_limits<uint64_t>::min();
    if (has_initial_) {
      initial = (uint64_t)initial_u64_;
    }
    struct Error err = kernel::reduce_max_64<uint64_t, uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_float32(const float* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<float> ptr = kernel::malloc<float>(
      ptr_lib, outlength*(int64_t)sizeof(float));
    float initial = -std::numeric_limits<float>::infinity();
    if (has_initial_) {
      initial = (float)initial_f64_;
    }
    struct Error err = kernel::reduce_max_64<float, float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_float64(const double* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<double> ptr = kernel::malloc<double>(
      ptr_lib, outlength*(int64_t)sizeof(double));
    double initial = -std::numeric_limits<double>::infinity();
    if (has_initial_) {
      initial = (double)initial_f64_;
    }
    struct Error err = kernel::reduce_max_64<double, double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_complex64(const std::complex<float>* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<float>> ptr = kernel::malloc<std::complex<float>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<float>));
    float initial = 0;
    if (has_initial_) {
      initial = (float)initial_f64_;
    }
    struct Error err = kernel::reduce_max_64<std::complex<float>, std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerMax::apply_complex128(const std::complex<double>* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<std::complex<double>> ptr = kernel::malloc<std::complex<double>>(
      ptr_lib, outlength*(int64_t)sizeof(std::complex<double>));
    double initial = 0;
    if (has_initial_) {
      initial = (double)initial_f64_;
    }
    struct Error err = kernel::reduce_max_64<std::complex<double>, std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength,
      initial);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// argmin (argument minimum, in which -1 is the identity)

  const std::string
  ReducerArgmin::name() const {
    return "argmin";
  }

  util::dtype
  ReducerArgmin::preferred_dtype() const {
    return util::dtype::int64;
  }

  util::dtype
  ReducerArgmin::return_dtype(util::dtype given_dtype) const {
    return util::dtype::int64;
  }

  bool
  ReducerArgmin::returns_positions() const {
    return true;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_bool(const bool* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_int8(const int8_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_uint8(const uint8_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_int16(const int16_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_uint16(const uint16_t* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_int32(const int32_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_uint32(const uint32_t* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_int64(const int64_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_uint64(const uint64_t* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_float32(const float* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_float64(const double* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_complex64(const std::complex<float>* data,
                                const Index64& parents,
                                int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmin::apply_complex128(const std::complex<double>* data,
                                  const Index64& parents,
                                  int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmin_64<int64_t, std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  ////////// argmax (argument maximum, in which -1 is the identity)

  const std::string
  ReducerArgmax::name() const {
    return "argmax";
  }

  util::dtype
  ReducerArgmax::preferred_dtype() const {
    return util::dtype::int64;
  }

  util::dtype
  ReducerArgmax::return_dtype(util::dtype given_dtype) const {
    return util::dtype::int64;
  }

  bool
  ReducerArgmax::returns_positions() const {
    return true;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_bool(const bool* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, bool>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_int8(const int8_t* data,
                            const Index64& parents,
                            int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, int8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_uint8(const uint8_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, uint8_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_int16(const int16_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, int16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_uint16(const uint16_t* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, uint16_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_int32(const int32_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, int32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_uint32(const uint32_t* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, uint32_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_int64(const int64_t* data,
                             const Index64& parents,
                             int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, int64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_uint64(const uint64_t* data,
                              const Index64& parents,
                              int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, uint64_t>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_float32(const float* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, float>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_float64(const double* data,
                               const Index64& parents,
                               int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, double>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_complex64(const std::complex<float>* data,
                                 const Index64& parents,
                                 int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, std::complex<float>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }

  const std::shared_ptr<void>
  ReducerArgmax::apply_complex128(const std::complex<double>* data,
                                  const Index64& parents,
                                  int64_t outlength) const {
    kernel::lib ptr_lib = kernel::lib::cpu;   // DERIVE
    std::shared_ptr<int64_t> ptr = kernel::malloc<int64_t>(
      ptr_lib, outlength*(int64_t)sizeof(int64_t));
    struct Error err = kernel::reduce_argmax_64<int64_t, std::complex<double>>(
      ptr_lib,
      ptr.get(),
      data,
      parents.data(),
      parents.length(),
      outlength);
    util::handle_error(err, util::quote(name()), nullptr);
    return ptr;
  }
}
