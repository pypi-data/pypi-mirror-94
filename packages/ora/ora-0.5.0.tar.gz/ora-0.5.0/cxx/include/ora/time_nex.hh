#pragma once

#include <cfenv>

#include "ora/lib/math.hh"
#include "ora/lib/num.hh"
#include "ora/time_math.hh"
#include "ora/time_type.hh"

namespace ora {
namespace time {
namespace nex {

//------------------------------------------------------------------------------
// Forward declarations
//------------------------------------------------------------------------------

template<class TIME> typename TIME::Offset get_offset(TIME) noexcept;

//------------------------------------------------------------------------------

template<class TIME=Time>
inline TIME
from_offset(
  typename TIME::Offset const offset)
  noexcept
{
  return 
      in_range(TIME::Traits::min, offset, TIME::Traits::max)
    ? TIME::from_offset(offset)
    : TIME::INVALID;
}


template<class TIME=Time, class FROM>
inline TIME
from_time(
  FROM const time)
  noexcept
{
  return
      time.is_invalid() ? TIME::INVALID
    : time.is_missing() ? TIME::MISSING
    : nex::from_offset<TIME>(
        // FIXME: This does not detect arithmetic overflow.
        convert_offset(
          nex::get_offset(time), 
          FROM::DENOMINATOR, FROM::BASE,
          TIME::DENOMINATOR, TIME::BASE));
}


template<class TIME=Time>
inline TIME
from_timespec(
  timespec const ts)
{
  return nex::from_offset(timespec_to_offset<TIME>(ts));
}


template<class TIME=Time>
inline bool
is_valid(
  TIME const time)
  noexcept
{
  return time.is_valid();
}


template<class TIME=Time>
inline typename TIME::Offset
get_offset(
  TIME const time)
  noexcept
{
  return time.offset_;
}


template<class TIME>
inline EpochTime
get_epoch_time(
  TIME const time)
  noexcept
{
  return
      time.is_valid() 
    ? convert_offset(
        nex::get_offset(time), TIME::DENOMINATOR, TIME::BASE,
        1, DATENUM_UNIX_EPOCH)
    : EPOCH_TIME_INVALID;
}


template<class TIME>
inline bool
equal(
  TIME const time0,
  TIME const time1)
  noexcept
{
  return nex::get_offset(time0) == nex::get_offset(time1);
}


template<class TIME>
inline bool
before(
  TIME const time0,
  TIME const time1)
  noexcept
{
  if (nex::equal(time0, time1))
    return false;
  else if (time0.is_invalid())
    return true;
  else if (time1.is_invalid())
    return false;
  else if (time0.is_missing())
    return true;
  else if (time1.is_missing())
    return false;
  else {
    assert(time0.is_valid());
    assert(time1.is_valid());
    return nex::get_offset(time0) < nex::get_offset(time1);
  }
}


template<class TIME>
inline int
compare(
  TIME const time0,
  TIME const time1)
{
  return
      nex::equal(time0, time1) ? 0
    : nex::before(time0, time1) ? -1
    : 1;
}


//------------------------------------------------------------------------------
// Arithmetic
//------------------------------------------------------------------------------

namespace {

template<class TIME>
inline TIME
seconds_shift(
  TIME const time,
  double const seconds,
  bool const forward)
{
  using Offset = typename TIME::Offset;

  if (time.is_valid() && !std::isnan(seconds) && !std::isinf(seconds)) {
    ora::num::Checked c;
    auto const offset = c.convert<Offset>(round(seconds * TIME::DENOMINATOR));
    if (c)
      return from_offset<TIME>(
        forward
        ? (nex::get_offset(time) + offset)
        : (nex::get_offset(time) - offset));
  }
  return TIME::INVALID;
}


template<class TIME>
inline TIME
seconds_shift(
  TIME const time,
  int64_t const seconds,
  bool const forward)
{
  using Offset = typename TIME::Offset;

  if (time.is_valid()) {
    auto const offset = rescale_int<Offset, 1, TIME::DENOMINATOR>(seconds);
    return from_offset<TIME>(
      forward
      ? (nex::get_offset(time) + offset)
      : (nex::get_offset(time) - offset));
  }
  else
    return TIME::INVALID;
}


}  // anonymous namespace

template<class TIME>
inline TIME
seconds_after(
  TIME const time,
  double const seconds)
  noexcept
{
  return seconds_shift<TIME>(time, std::abs(seconds), seconds > 0);
}


template<class TIME>
inline TIME
seconds_after(
  TIME const time,
  int64_t const seconds)
  noexcept
{
  return seconds_shift<TIME>(time, std::abs(seconds), seconds > 0);
}


template<class TIME>
inline TIME
seconds_before(
  TIME const time,
  double const seconds)
  noexcept
{
  return seconds_shift<TIME>(time, std::abs(seconds), seconds < 0);
}


template<class TIME>
inline TIME
seconds_before(
  TIME const time,
  int64_t const seconds)
  noexcept
{
  return seconds_shift<TIME>(time, std::abs(seconds), seconds < 0);
}


template<class TIME>
inline double
seconds_between(
  TIME const time0,
  TIME const time1)
  noexcept
{
  if (! (time0.is_valid() && time1.is_valid()))
    return std::numeric_limits<double>::quiet_NaN();

  auto const off0 = nex::get_offset(time0);
  auto const off1 = nex::get_offset(time1);
  // Needs to work for unsigned offsets.
  return
      off1 >= off0
    ?   (off1 - off0) * TIME::RESOLUTION
    : -((off0 - off1) * TIME::RESOLUTION);
}


}  // namespace nex

//------------------------------------------------------------------------------
// Comparison operators
//------------------------------------------------------------------------------

template<class T0, class T1> inline bool operator==(TimeType<T0> const t0, TimeType<T1> const t1) noexcept
  { return nex::equal(t0, TimeType<T0>(t1)); }
template<class T0, class T1> inline bool operator!=(TimeType<T0> const t0, TimeType<T1> const t1) noexcept
  { return !nex::equal(t0, TimeType<T0>(t1)); }
template<class T0, class T1> inline bool operator< (TimeType<T0> const t0, TimeType<T1> const t1) noexcept
  { return nex::before(t0, TimeType<T0>(t1)); }
template<class T0, class T1> inline bool operator> (TimeType<T0> const t0, TimeType<T1> const t1) noexcept
  { return nex::before(TimeType<T0>(t1), t0); }
template<class T0, class T1> inline bool operator<=(TimeType<T0> const t0, TimeType<T1> const t1) noexcept
  { return !nex::before(TimeType<T0>(t1), t0); }
template<class T0, class T1> inline bool operator>=(TimeType<T0> const t0, TimeType<T1> const t1) noexcept
  { return !nex::before(t0, TimeType<T0>(t1)); }

//------------------------------------------------------------------------------

}  // namespace time
}  // namespace ora

