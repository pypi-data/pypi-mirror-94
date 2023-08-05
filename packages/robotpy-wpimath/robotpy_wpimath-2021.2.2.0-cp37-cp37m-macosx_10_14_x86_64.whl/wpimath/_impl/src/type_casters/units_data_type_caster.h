#pragma once

#include <units/data.h>

namespace pybind11 {
namespace detail {
template <> struct handle_type_name<units::exabyte_t> {
  static constexpr auto name = _("exabytes");
};

template <> struct handle_type_name<units::exabytes> {
  static constexpr auto name = _("exabytes");
};

template <> struct handle_type_name<units::exabit_t> {
  static constexpr auto name = _("exabits");
};

template <> struct handle_type_name<units::exabits> {
  static constexpr auto name = _("exabits");
};

} // namespace detail
} // namespace pybind11

#include "_units_base_type_caster.h"
