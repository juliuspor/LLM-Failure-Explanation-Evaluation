# -*- coding: utf-8 -*-
"""
DateTimeZone - Represents a time zone.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Dict, Set, Any
from datetime import datetime, timezone
import re
import pickle
import time
import os


class IllegalInstantException(Exception):
    """Exception thrown when an instant is illegal in a time zone."""
    
    def __init__(self, instant_local: int, zone_id: str):
        self.instant_local = instant_local
        self.zone_id = zone_id
        super().__init__(f"Illegal instant due to time zone offset transition "
                        f"(daylight savings time 'gap'): {zone_id}")


class DateTimeConstants:
    """Constants used throughout the datetime classes."""
    MILLIS_PER_SECOND = 1000
    MILLIS_PER_MINUTE = 60000
    MILLIS_PER_HOUR = 3600000
    MILLIS_PER_DAY = 86400000


class ReadableInstant(ABC):
    """Abstract interface for an instant in time."""
    
    @abstractmethod
    def get_millis(self) -> int:
        """Gets the millisecond instant from 1970-01-01T00:00:00Z."""
        pass


class LocalDateTime:
    """A local date-time without a time zone."""
    
    def __init__(self, millis: int):
        self._millis = millis
    
    def get_millis(self) -> int:
        return self._millis
    
    def to_datetime(self, zone: 'DateTimeZone') -> 'DateTime':
        """Converts this local datetime to a DateTime in the given zone."""
        instant_local = self._millis
        instant_utc = zone.convert_local_to_utc(instant_local, True)
        return DateTime(instant_utc, zone)


class DateTime(ReadableInstant):
    """A datetime with a time zone."""
    
    def __init__(self, millis: int, zone: 'DateTimeZone'):
        self._millis = millis
        self._zone = zone
    
    def get_millis(self) -> int:
        return self._millis
    
    def get_zone(self) -> 'DateTimeZone':
        return self._zone


class DateTimeUtils:
    """Utility methods for datetime operations."""
    
    @staticmethod
    def current_time_millis() -> int:
        """Gets the current time in milliseconds since epoch."""
        return int(time.time() * 1000)


class FieldUtils:
    """Utility methods for field manipulation."""
    
    @staticmethod
    def safe_multiply(val1: int, val2: int) -> int:
        """
        Multiplies two values throwing an exception if overflow occurs.
        
        Args:
            val1: the first value
            val2: the second value
            
        Returns:
            the result
            
        Raises:
            ArithmeticError: if multiplication overflows
        """
        total = val1 * val2
        if val2 != 0 and total // val2 != val1:
            raise ArithmeticError(f"Multiplication overflows: {val1} * {val2}")
        return total


class FormatUtils:
    """Utility methods for formatting."""
    
    @staticmethod
    def append_padded_integer(buf: list, value: int, size: int) -> None:
        """Appends a padded integer to the buffer."""
        s = str(value)
        while len(s) < size:
            s = '0' + s
        buf.append(s)


class Provider(ABC):
    """Interface for providing DateTimeZone instances."""
    
    @abstractmethod
    def get_zone(self, zone_id: str) -> Optional['DateTimeZone']:
        """Gets a zone by ID."""
        pass
    
    @abstractmethod
    def get_available_ids(self) -> Set[str]:
        """Gets all available zone IDs."""
        pass


class NameProvider(ABC):
    """Interface for providing DateTimeZone names."""
    
    @abstractmethod
    def get_short_name(self, locale: str, zone_id: str, name_key: str) -> Optional[str]:
        """Gets the short name for a zone."""
        pass
    
    @abstractmethod
    def get_name(self, locale: str, zone_id: str, name_key: str) -> Optional[str]:
        """Gets the long name for a zone."""
        pass


class UTCProvider(Provider):
    """Provider that only provides UTC."""
    
    def get_zone(self, zone_id: str) -> Optional['DateTimeZone']:
        if zone_id == "UTC":
            return DateTimeZone.UTC
        return None
    
    def get_available_ids(self) -> Set[str]:
        return {"UTC"}


class DefaultNameProvider(NameProvider):
    """Default name provider implementation."""
    
    def get_short_name(self, locale: str, zone_id: str, name_key: str) -> Optional[str]:
        return None
    
    def get_name(self, locale: str, zone_id: str, name_key: str) -> Optional[str]:
        return None


class DateTimeZone(ABC):
    """
    DateTimeZone represents a time zone.
    
    A time zone is a system of rules to convert time from one geographic 
    location to another. For example, Paris, France is one hour ahead of
    London, England. Thus when it is 10:00 in London, it is 11:00 in Paris.
    
    All time zone rules are expressed, for historical reasons, relative to
    Greenwich, London. Local time in Greenwich is referred to as Greenwich Mean
    Time (GMT). This is similar, but not precisely identical, to Universal 
    Coordinated Time, or UTC. This library only uses the term UTC.
    
    Using this system, America/Los_Angeles is expressed as UTC-08:00, or UTC-07:00
    in the summer. The offset -08:00 indicates that America/Los_Angeles time is
    obtained from UTC by adding -08:00, that is, by subtracting 8 hours.
    
    The offset differs in the summer because of daylight saving time, or DST.
    The following definitions of time are generally used:
    - UTC - The reference time.
    - Standard Time - The local time without a daylight saving time offset.
      For example, in Paris, standard time is UTC+01:00.
    - Daylight Saving Time - The local time with a daylight saving time 
      offset. This offset is typically one hour, but not always. It is typically
      used in most countries away from the equator. In Paris, daylight saving 
      time is UTC+02:00.
    - Wall Time - This is what a local clock on the wall reads. This will be
      either Standard Time or Daylight Saving Time depending on the time of year
      and whether the location uses Daylight Saving Time.
    
    Unlike the Java TimeZone class, DateTimeZone is immutable. It also only
    supports long format time zone ids. Thus EST and ECT are not accepted.
    However, the factory that accepts a TimeZone will attempt to convert from
    the old short id to a suitable long id.
    
    DateTimeZone is thread-safe and immutable, and all subclasses must be as well.
    """
    
    # Class constants
    UTC: 'DateTimeZone' = None  # Will be set after class definition
    _MAX_MILLIS = (86400 * 1000) - 1
    
    # Static fields
    _provider: Provider = None
    _name_provider: NameProvider = None
    _available_ids: Set[str] = None
    _default: 'DateTimeZone' = None
    
    # Cache that maps fixed offset strings to DateTimeZones
    _fixed_offset_cache: Dict[str, 'DateTimeZone'] = {}
    
    # Cache of old zone IDs to new zone IDs
    _zone_id_conversion: Dict[str, str] = None
    
    @classmethod
    def _init_static(cls):
        """Initialize static fields."""
        cls._set_provider0(None)
        cls._set_name_provider0(None)
    
    # -----------------------------------------------------------------------
    @classmethod
    def get_default(cls) -> 'DateTimeZone':
        """
        Gets the default time zone.
        
        The default time zone is derived from the system environment.
        If that is null or is not a valid identifier, UTC is used.
        
        Returns:
            the default datetime zone object
        """
        zone = cls._default
        if zone is None:
            temp = None
            try:
                try:
                    zone_id = os.environ.get('TZ')
                    if zone_id is not None:
                        temp = cls.for_id(zone_id)
                except RuntimeError:
                    pass
                if temp is None:
                    # Try to use Python's local timezone
                    try:
                        import time as time_module
                        if time_module.daylight:
                            zone_name = time_module.tzname[1]
                        else:
                            zone_name = time_module.tzname[0]
                        temp = cls.for_id(zone_name)
                    except (ValueError, KeyError):
                        pass
            except ValueError:
                pass
            if temp is None:
                temp = cls.UTC
            cls._default = temp
            zone = temp
        return zone
    
    @classmethod
    def set_default(cls, zone: 'DateTimeZone') -> None:
        """
        Sets the default time zone.
        
        Args:
            zone: the default datetime zone object, must not be None
            
        Raises:
            ValueError: if the zone is None
        """
        if zone is None:
            raise ValueError("The datetime zone must not be null")
        cls._default = zone
    
    # -----------------------------------------------------------------------
    @classmethod
    def for_id(cls, zone_id: str) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified time zone id.
        
        The time zone id may be one of those returned by get_available_ids.
        Short ids, as accepted by java.util.TimeZone, are not accepted.
        All IDs must be specified in the long format.
        The exception is UTC, which is an acceptable id.
        
        Alternatively a locale independent, fixed offset, datetime zone can
        be specified. The form [+-]hh:mm can be used.
        
        Args:
            zone_id: the ID of the datetime zone, None means default
            
        Returns:
            the DateTimeZone object for the ID
            
        Raises:
            ValueError: if the ID is not recognised
        """
        if zone_id is None:
            return cls.get_default()
        if zone_id == "UTC":
            return cls.UTC
        zone = cls._provider.get_zone(zone_id)
        if zone is not None:
            return zone
        if zone_id.startswith("+") or zone_id.startswith("-"):
            offset = cls._parse_offset(zone_id)
            if offset == 0:
                return cls.UTC
            else:
                zone_id = cls._print_offset(offset)
                return cls._fixed_offset_zone(zone_id, offset)
        raise ValueError(f"The datetime zone id '{zone_id}' is not recognised")
    
    @classmethod
    def for_offset_hours(cls, hours_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours.
        This method assumes standard length hours.
        
        This factory is a convenient way of constructing zones with a fixed offset.
        
        Args:
            hours_offset: the offset in hours from UTC, from -23 to +23
            
        Returns:
            the DateTimeZone object for the offset
            
        Raises:
            ValueError: if the offset is too large or too small
        """
        return cls.for_offset_hours_minutes(hours_offset, 0)
    
    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if abs(minutes_offset) > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Sign of minutes must match sign of hours")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError("Sign of minutes must match sign of hours")
        try:
            total_minutes = hours_offset * 60 + minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
    
    @classmethod
    def for_offset_millis(cls, millis_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in milliseconds.
        
        Args:
            millis_offset: the offset in millis from UTC, from -23:59:59.999 to +23:59:59.999
            
        Returns:
            the DateTimeZone object for the offset
        """
        if millis_offset < -cls._MAX_MILLIS or millis_offset > cls._MAX_MILLIS:
            raise ValueError(f"Millis out of range: {millis_offset}")
        zone_id = cls._print_offset(millis_offset)
        return cls._fixed_offset_zone(zone_id, millis_offset)
    
    @classmethod
    def for_time_zone(cls, tz: Any) -> 'DateTimeZone':
        """
        Gets a time zone instance for a Python timezone object.
        
        DateTimeZone only accepts a subset of the IDs from TimeZone. The
        excluded IDs are the short three letter form (except UTC). This 
        method will attempt to convert between time zones created using the
        short IDs and the full version.
        
        Args:
            tz: the timezone to convert, None means default
            
        Returns:
            the DateTimeZone object for the zone
            
        Raises:
            ValueError: if the zone is not recognised
        """
        if tz is None:
            return cls.get_default()
        
        # Handle Python timezone objects
        if hasattr(tz, 'key'):
            zone_id = tz.key
        elif hasattr(tz, 'zone'):
            zone_id = tz.zone
        else:
            zone_id = str(tz)
        
        if zone_id == "UTC":
            return cls.UTC
        
        # Convert from old alias before consulting provider since they may differ.
        dtz = None
        conv_id = cls._get_converted_id(zone_id)
        if conv_id is not None:
            dtz = cls._provider.get_zone(conv_id)
        if dtz is None:
            dtz = cls._provider.get_zone(zone_id)
        if dtz is not None:
            return dtz
        
        # Support GMT+/-hh:mm formats
        if conv_id is None:
            conv_id = zone_id
            if conv_id.startswith("GMT+") or conv_id.startswith("GMT-"):
                conv_id = conv_id[3:]
                offset = cls._parse_offset(conv_id)
                if offset == 0:
                    return cls.UTC
                else:
                    conv_id = cls._print_offset(offset)
                    return cls._fixed_offset_zone(conv_id, offset)
        raise ValueError(f"The datetime zone id '{zone_id}' is not recognised")
    
    # -----------------------------------------------------------------------
    @classmethod
    def _fixed_offset_zone(cls, zone_id: str, offset: int) -> 'DateTimeZone':
        """
        Gets the zone using a fixed offset amount.
        
        Args:
            zone_id: the zone id
            offset: the offset in millis
            
        Returns:
            the zone
        """
        if offset == 0:
            return cls.UTC
        if zone_id in cls._fixed_offset_cache:
            return cls._fixed_offset_cache[zone_id]
        zone = FixedDateTimeZone(zone_id, None, offset, offset)
        cls._fixed_offset_cache[zone_id] = zone
        return zone
    
    @classmethod
    def get_available_ids(cls) -> Set[str]:
        """
        Gets all the available IDs supported.
        
        Returns:
            an unmodifiable Set of String IDs
        """
        return frozenset(cls._available_ids)
    
    # -----------------------------------------------------------------------
    @classmethod
    def get_provider(cls) -> Provider:
        """
        Gets the zone provider factory.
        
        The zone provider is a pluggable instance factory that supplies the
        actual instances of DateTimeZone.
        
        Returns:
            the provider
        """
        return cls._provider
    
    @classmethod
    def set_provider(cls, provider: Provider) -> None:
        """
        Sets the zone provider factory.
        
        The zone provider is a pluggable instance factory that supplies the
        actual instances of DateTimeZone.
        
        Args:
            provider: provider to use, or None for default
            
        Raises:
            ValueError: if the provider is invalid
        """
        cls._set_provider0(provider)
    
    @classmethod
    def _set_provider0(cls, provider: Provider) -> None:
        """
        Sets the zone provider factory without performing the security check.
        
        Args:
            provider: provider to use, or None for default
            
        Raises:
            ValueError: if the provider is invalid
        """
        if provider is None:
            provider = cls._get_default_provider()
        ids = provider.get_available_ids()
        if ids is None or len(ids) == 0:
            raise ValueError("The provider doesn't have any available ids")
        if "UTC" not in ids:
            raise ValueError("The provider doesn't support UTC")
        if cls.UTC is not None and cls.UTC != provider.get_zone("UTC"):
            raise ValueError("Invalid UTC zone provided")
        cls._provider = provider
        cls._available_ids = ids
    
    @classmethod
    def _get_default_provider(cls) -> Provider:
        """
        Gets the default zone provider.
        
        Returns:
            the default provider
        """
        return UTCProvider()
    
    # -----------------------------------------------------------------------
    @classmethod
    def get_name_provider(cls) -> NameProvider:
        """
        Gets the name provider factory.
        
        The name provider is a pluggable instance factory that supplies the
        names of each DateTimeZone.
        
        Returns:
            the provider
        """
        return cls._name_provider
    
    @classmethod
    def set_name_provider(cls, name_provider: NameProvider) -> None:
        """
        Sets the name provider factory.
        
        The name provider is a pluggable instance factory that supplies the
        names of each DateTimeZone.
        
        Args:
            name_provider: provider to use, or None for default
        """
        cls._set_name_provider0(name_provider)
    
    @classmethod
    def _set_name_provider0(cls, name_provider: NameProvider) -> None:
        """
        Sets the name provider factory without performing the security check.
        
        Args:
            name_provider: provider to use, or None for default
        """
        if name_provider is None:
            name_provider = cls._get_default_name_provider()
        cls._name_provider = name_provider
    
    @classmethod
    def _get_default_name_provider(cls) -> NameProvider:
        """
        Gets the default name provider.
        
        Returns:
            the default name provider
        """
        return DefaultNameProvider()
    
    # -----------------------------------------------------------------------
    @classmethod
    def _get_converted_id(cls, zone_id: str) -> Optional[str]:
        """
        Converts an old style id to a new style id.
        
        Args:
            zone_id: the old style id
            
        Returns:
            the new style id, None if not found
        """
        if cls._zone_id_conversion is None:
            # Backwards compatibility with TimeZone
            conversion_map = {
                "GMT": "UTC",
                "WET": "WET",
                "CET": "CET",
                "MET": "CET",
                "ECT": "CET",
                "EET": "EET",
                "MIT": "Pacific/Apia",
                "HST": "Pacific/Honolulu",
                "AST": "America/Anchorage",
                "PST": "America/Los_Angeles",
                "MST": "America/Denver",
                "PNT": "America/Phoenix",
                "CST": "America/Chicago",
                "EST": "America/New_York",
                "IET": "America/Indiana/Indianapolis",
                "PRT": "America/Puerto_Rico",
                "CNT": "America/St_Johns",
                "AGT": "America/Argentina/Buenos_Aires",
                "BET": "America/Sao_Paulo",
                "ART": "Africa/Cairo",
                "CAT": "Africa/Harare",
                "EAT": "Africa/Addis_Ababa",
                "NET": "Asia/Yerevan",
                "PLT": "Asia/Karachi",
                "IST": "Asia/Kolkata",
                "BST": "Asia/Dhaka",
                "VST": "Asia/Ho_Chi_Minh",
                "CTT": "Asia/Shanghai",
                "JST": "Asia/Tokyo",
                "ACT": "Australia/Darwin",
                "AET": "Australia/Sydney",
                "SST": "Pacific/Guadalcanal",
                "NST": "Pacific/Auckland",
            }
            cls._zone_id_conversion = conversion_map
        return cls._zone_id_conversion.get(zone_id)
    
    @classmethod
    def _parse_offset(cls, offset_str: str) -> int:
        """
        Parses an offset string like +02:15 or -02:15.
        
        Args:
            offset_str: the offset string to parse
            
        Returns:
            the offset in milliseconds
        """
        # Parse format: +HH:MM or -HH:MM or +HH:MM:SS or +HH:MM:SS.mmm
        match = re.match(r'^([+-])(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{3}))?)?$', offset_str)
        if not match:
            raise ValueError(f"Invalid offset format: {offset_str}")
        sign = -1 if match.group(1) == '-' else 1
        hours = int(match.group(2))
        minutes = int(match.group(3))
        seconds = int(match.group(4)) if match.group(4) else 0
        millis = int(match.group(5)) if match.group(5) else 0
        
        total_millis = (hours * DateTimeConstants.MILLIS_PER_HOUR +
                       minutes * DateTimeConstants.MILLIS_PER_MINUTE +
                       seconds * DateTimeConstants.MILLIS_PER_SECOND +
                       millis)
        return sign * total_millis
    
    @classmethod
    def _print_offset(cls, offset: int) -> str:
        """
        Formats a timezone offset string.
        
        This method is kept separate from the formatting classes to speed and
        simplify startup and classloading.
        
        Args:
            offset: the offset in milliseconds
            
        Returns:
            the time zone string
        """
        buf = []
        if offset >= 0:
            buf.append('+')
        else:
            buf.append('-')
            offset = -offset
        
        hours = offset // DateTimeConstants.MILLIS_PER_HOUR
        FormatUtils.append_padded_integer(buf, hours, 2)
        offset -= hours * DateTimeConstants.MILLIS_PER_HOUR
        
        minutes = offset // DateTimeConstants.MILLIS_PER_MINUTE
        buf.append(':')
        FormatUtils.append_padded_integer(buf, minutes, 2)
        offset -= minutes * DateTimeConstants.MILLIS_PER_MINUTE
        if offset == 0:
            return ''.join(buf)
        
        seconds = offset // DateTimeConstants.MILLIS_PER_SECOND
        buf.append(':')
        FormatUtils.append_padded_integer(buf, seconds, 2)
        offset -= seconds * DateTimeConstants.MILLIS_PER_SECOND
        if offset == 0:
            return ''.join(buf)
        
        buf.append('.')
        FormatUtils.append_padded_integer(buf, offset, 3)
        return ''.join(buf)
    
    # Instance fields and methods
    # --------------------------------------------------------------------
    
    def __init__(self, zone_id: str):
        """
        Constructor.
        
        Args:
            zone_id: the id to use
            
        Raises:
            ValueError: if the id is None
        """
        if zone_id is None:
            raise ValueError("Id must not be null")
        self._id = zone_id
    
    # Principal methods
    # --------------------------------------------------------------------
    
    @property
    def id(self) -> str:
        """Gets the ID of this datetime zone."""
        return self._id
    
    def get_id(self) -> str:
        """Gets the ID of this datetime zone."""
        return self._id
    
    @abstractmethod
    def get_name_key(self, instant: int) -> Optional[str]:
        """
        Returns a non-localized name that is unique to this time zone. It can be
        combined with id to form a unique key for fetching localized names.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z to get the name for
            
        Returns:
            name key or None if id should be used for names
        """
        pass
    
    def get_short_name(self, instant: int, locale: str = None) -> str:
        """
        Gets the short name of this datetime zone suitable for display using
        the specified locale.
        
        If the name is not available for the locale, then this method returns a
        string in the format [+-]hh:mm.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z to get the name for
            locale: the locale to get the name for
            
        Returns:
            the human-readable short name in the specified locale
        """
        if locale is None:
            import locale as locale_module
            locale = locale_module.getdefaultlocale()[0]
        name_key = self.get_name_key(instant)
        if name_key is None:
            return self._id
        name = self._name_provider.get_short_name(locale, self._id, name_key)
        if name is not None:
            return name
        return self._print_offset(self.get_offset(instant))
    
    def get_name(self, instant: int, locale: str = None) -> str:
        """
        Gets the long name of this datetime zone suitable for display using
        the specified locale.
        
        If the name is not available for the locale, then this method returns a
        string in the format [+-]hh:mm.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z to get the name for
            locale: the locale to get the name for
            
        Returns:
            the human-readable long name in the specified locale
        """
        if locale is None:
            import locale as locale_module
            locale = locale_module.getdefaultlocale()[0]
        name_key = self.get_name_key(instant)
        if name_key is None:
            return self._id
        name = self._name_provider.get_name(locale, self._id, name_key)
        if name is not None:
            return name
        return self._print_offset(self.get_offset(instant))
    
    @abstractmethod
    def get_offset(self, instant: int) -> int:
        """
        Gets the millisecond offset to add to UTC to get local time.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z to get the offset for
            
        Returns:
            the millisecond offset to add to UTC to get local time
        """
        pass
    
    def get_offset_from_instant(self, instant: ReadableInstant) -> int:
        """
        Gets the millisecond offset to add to UTC to get local time.
        
        Args:
            instant: instant to get the offset for, None means now
            
        Returns:
            the millisecond offset to add to UTC to get local time
        """
        if instant is None:
            return self.get_offset(DateTimeUtils.current_time_millis())
        return self.get_offset(instant.get_millis())
    
    @abstractmethod
    def get_standard_offset(self, instant: int) -> int:
        """
        Gets the standard millisecond offset to add to UTC to get local time,
        when standard time is in effect.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z to get the offset for
            
        Returns:
            the millisecond offset to add to UTC to get local time
        """
        pass
    
    def is_standard_offset(self, instant: int) -> bool:
        """
        Checks whether, at a particular instant, the offset is standard or not.
        
        This method can be used to determine whether Summer Time (DST) applies.
        As a general rule, if the offset at the specified instant is standard,
        then either Winter time applies, or there is no Summer Time. If the
        instant is not standard, then Summer Time applies.
        
        The implementation of the method is simply whether get_offset(instant)
        equals get_standard_offset(instant) at the specified instant.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z to get the offset for
            
        Returns:
            True if the offset at the given instant is the standard offset
        """
        return self.get_offset(instant) == self.get_standard_offset(instant)
    
    def get_offset_from_local(self, instant_local: int) -> int:
        """
        Gets the millisecond offset to subtract from local time to get UTC time.
        This offset can be used to undo adding the offset obtained by get_offset.
        
        millisLocal == millisUTC   + get_offset(millisUTC)
        millisUTC   == millisLocal - get_offset_from_local(millisLocal)
        
        NOTE: After calculating millisLocal, some error may be introduced. At
        offset transitions (due to DST or other historical changes), ranges of
        local times may map to different UTC times.
        
        This method will return an offset suitable for calculating an instant
        after any DST gap.
        
        During a DST overlap (where the local time is ambiguous) this method will return
        the earlier instant. The combination of these two rules is to always favour
        daylight (summer) time over standard (winter) time.
        
        Args:
            instant_local: the millisecond instant, relative to this time zone, to get the offset for
            
        Returns:
            the millisecond offset to subtract from local time to get UTC time
        """
        # get the offset at instant_local (first estimate)
        offset_local = self.get_offset(instant_local)
        # adjust instant_local using the estimate and recalc the offset
        instant_adjusted = instant_local - offset_local
        offset_adjusted = self.get_offset(instant_adjusted)
        # if the offsets differ, we must be near a DST boundary
        if offset_local != offset_adjusted:
            # we need to ensure that time is always after the DST gap
            # this happens naturally for positive offsets, but not for negative
            if (offset_local - offset_adjusted) < 0:
                # if we just return offset_adjusted then the time is pushed
                # back before the transition, whereas it should be
                # on or after the transition
                next_local = self.next_transition(instant_adjusted)
                next_adjusted = self.next_transition(instant_local - offset_adjusted)
                if next_local != next_adjusted:
                    return offset_local
        elif offset_local >= 0:
            prev = self.previous_transition(instant_adjusted)
            if prev < instant_adjusted:
                offset_prev = self.get_offset(prev)
                diff = offset_prev - offset_local
                if instant_adjusted - prev <= diff:
                    return offset_prev
        return offset_adjusted
    
    def convert_utc_to_local(self, instant_utc: int) -> int:
        """
        Converts a standard UTC instant to a local instant with the same
        local time. This conversion is used before performing a calculation
        so that the calculation can be done using a simple local zone.
        
        Args:
            instant_utc: the UTC instant to convert to local
            
        Returns:
            the local instant with the same local time
            
        Raises:
            ArithmeticError: if the result overflows
        """
        offset = self.get_offset(instant_utc)
        instant_local = instant_utc + offset
        # If there is a sign change, but the two values have the same sign...
        if (instant_utc ^ instant_local) < 0 and (instant_utc ^ offset) >= 0:
            raise ArithmeticError("Adding time zone offset caused overflow")
        return instant_local
    
    def convert_local_to_utc(self, instant_local: int, strict: bool, original_instant_utc: int = None) -> int:
        """
        Converts a local instant to a standard UTC instant with the same
        local time attempting to use the same offset as the original.
        
        This conversion is used after performing a calculation
        where the calculation was done using a simple local zone.
        Whenever possible, the same offset as the original offset will be used.
        This is most significant during a daylight savings overlap.
        
        Args:
            instant_local: the local instant to convert to UTC
            strict: whether the conversion should reject non-existent local times
            original_instant_utc: the original instant that the calculation is based on (optional)
            
        Returns:
            the UTC instant with the same local time
            
        Raises:
            ArithmeticError: if the result overflows
            IllegalInstantException: if the zone has no equivalent local time
        """
        if original_instant_utc is not None:
            offset_original = self.get_offset(original_instant_utc)
            instant_utc = instant_local - offset_original
            offset_local_from_original = self.get_offset(instant_utc)
            if offset_local_from_original == offset_original:
                return instant_utc
            # Fall through to non-original path
        
        # get the offset at instant_local (first estimate)
        offset_local = self.get_offset(instant_local)
        # adjust instant_local using the estimate and recalc the offset
        offset = self.get_offset(instant_local - offset_local)
        # if the offsets differ, we must be near a DST boundary
        if offset_local != offset:
            # if strict then always check if in DST gap
            # otherwise only check if zone in Western hemisphere (as the
            # value of offset is already correct for Eastern hemisphere)
            if strict or offset_local < 0:
                # determine if we are in the DST gap
                next_local = self.next_transition(instant_local - offset_local)
                if next_local == (instant_local - offset_local):
                    next_local = 2**63 - 1  # Long.MAX_VALUE equivalent
                next_adjusted = self.next_transition(instant_local - offset)
                if next_adjusted == (instant_local - offset):
                    next_adjusted = 2**63 - 1
                if next_local != next_adjusted:
                    # yes we are in the DST gap
                    if strict:
                        # DST gap is not acceptable
                        raise IllegalInstantException(instant_local, self.get_id())
                    else:
                        # DST gap is acceptable, but for the Western hemisphere
                        # the offset is wrong and will result in local times
                        # before the cutover so use the offset_local instead
                        offset = offset_local
        
        # check for overflow
        instant_utc = instant_local - offset
        # If there is a sign change, but the two values have different signs...
        if (instant_local ^ instant_utc) < 0 and (instant_local ^ offset) < 0:
            raise ArithmeticError("Subtracting time zone offset caused overflow")
        return instant_utc
    
    def get_millis_keep_local(self, new_zone: 'DateTimeZone', old_instant: int) -> int:
        """
        Gets the millisecond instant in another zone keeping the same local time.
        
        The conversion is performed by converting the specified UTC millis to local
        millis in this zone, then converting back to UTC millis in the new zone.
        
        Args:
            new_zone: the new zone, None means default
            old_instant: the UTC millisecond instant to convert
            
        Returns:
            the UTC millisecond instant with the same local time in the new zone
        """
        if new_zone is None:
            new_zone = DateTimeZone.get_default()
        if new_zone == self:
            return old_instant
        instant_local = self.convert_utc_to_local(old_instant)
        return new_zone.convert_local_to_utc(instant_local, False, old_instant)
    
    def is_local_datetime_gap(self, local_datetime: LocalDateTime) -> bool:
        """
        Checks if the given LocalDateTime is within a gap.
        
        When switching from standard time to Daylight Savings Time there is
        typically a gap where a clock hour is missing. This method identifies
        whether the local datetime refers to such a gap.
        
        Args:
            local_datetime: the time to check, not None
            
        Returns:
            True if the given datetime refers to a gap
        """
        if self.is_fixed():
            return False
        try:
            local_datetime.to_datetime(self)
            return False
        except IllegalInstantException:
            return True
    
    def adjust_offset(self, instant: int, earlier_or_later: bool) -> int:
        """
        Adjusts the offset to be the earlier or later one during an overlap.
        
        Args:
            instant: the instant to adjust
            earlier_or_later: False for earlier, True for later
            
        Returns:
            the adjusted instant millis
        """
        # a bit messy, but will work in all non-pathological cases
        
        # evaluate 3 hours before and after to work out if anything is happening
        instant_before = instant - 3 * DateTimeConstants.MILLIS_PER_HOUR
        instant_after = instant + 3 * DateTimeConstants.MILLIS_PER_HOUR
        offset_before = self.get_offset(instant_before)
        offset_after = self.get_offset(instant_after)
        if offset_before <= offset_after:
            return instant  # not an overlap (less than is a gap, equal is normal case)
        
        # work out range of instants that have duplicate local times
        diff = offset_before - offset_after
        transition = self.next_transition(instant_before)
        overlap_start = transition - diff
        overlap_end = transition + diff
        if instant < overlap_start or instant >= overlap_end:
            return instant  # not an overlap
        
        # calculate result
        after_start = instant - overlap_start
        if after_start >= diff:
            # currently in later offset
            return instant if earlier_or_later else instant - diff
        else:
            # currently in earlier offset
            return instant + diff if earlier_or_later else instant
    
    # -----------------------------------------------------------------------
    @abstractmethod
    def is_fixed(self) -> bool:
        """
        Returns True if this time zone has no transitions.
        
        Returns:
            True if no transitions
        """
        pass
    
    @abstractmethod
    def next_transition(self, instant: int) -> int:
        """
        Advances the given instant to where the time zone offset or name changes.
        If the instant returned is exactly the same as passed in, then
        no changes occur after the given instant.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z
            
        Returns:
            milliseconds from 1970-01-01T00:00:00Z
        """
        pass
    
    @abstractmethod
    def previous_transition(self, instant: int) -> int:
        """
        Retreats the given instant to where the time zone offset or name changes.
        If the instant returned is exactly the same as passed in, then
        no changes occur before the given instant.
        
        Args:
            instant: milliseconds from 1970-01-01T00:00:00Z
            
        Returns:
            milliseconds from 1970-01-01T00:00:00Z
        """
        pass
    
    # Basic methods
    # --------------------------------------------------------------------
    
    def to_time_zone(self) -> timezone:
        """
        Get the datetime zone as a Python timezone.
        
        Returns:
            the closest matching timezone object
        """
        from datetime import timedelta
        offset_millis = self.get_offset(DateTimeUtils.current_time_millis())
        return timezone(timedelta(milliseconds=offset_millis))
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        """
        Compare this datetime zone with another.
        
        Args:
            other: the object to compare with
            
        Returns:
            True if equal, based on the ID and all internal rules
        """
        pass
    
    def __hash__(self) -> int:
        """
        Gets a hash code compatible with equals.
        
        Returns:
            suitable hashcode
        """
        return 57 + hash(self.get_id())
    
    def __str__(self) -> str:
        """
        Gets the datetime zone as a string, which is simply its ID.
        
        Returns:
            the id of the zone
        """
        return self.get_id()
    
    def __repr__(self) -> str:
        return f"DateTimeZone[{self.get_id()}]"
    
    def __reduce__(self):
        """
        Support for pickle serialization.
        By default, when DateTimeZones are serialized, only a "stub" object
        referring to the id is written out. When the stub is read in, it
        replaces itself with a DateTimeZone object.
        """
        return (_unpickle_zone, (self._id,))


def _unpickle_zone(zone_id: str) -> DateTimeZone:
    """Helper function for unpickling DateTimeZone objects."""
    return DateTimeZone.for_id(zone_id)


class FixedDateTimeZone(DateTimeZone):
    """
    A DateTimeZone with a fixed offset.
    
    This implementation maintains a constant offset from UTC at all times.
    """
    
    def __init__(self, zone_id: str, name_key: Optional[str], wall_offset: int, standard_offset: int):
        """
        Constructor.
        
        Args:
            zone_id: the id of the zone
            name_key: the name key for the zone
            wall_offset: the wall offset in millis
            standard_offset: the standard offset in millis
        """
        super().__init__(zone_id)
        self._name_key = name_key
        self._wall_offset = wall_offset
        self._standard_offset = standard_offset
    
    def get_name_key(self, instant: int) -> Optional[str]:
        """Returns the name key."""
        return self._name_key
    
    def get_offset(self, instant: int) -> int:
        """Returns the wall offset."""
        return self._wall_offset
    
    def get_standard_offset(self, instant: int) -> int:
        """Returns the standard offset."""
        return self._standard_offset
    
    def get_offset_from_local(self, instant_local: int) -> int:
        """Returns the wall offset (constant for fixed zones)."""
        return self._wall_offset
    
    def is_fixed(self) -> bool:
        """Returns True since this is a fixed zone."""
        return True
    
    def next_transition(self, instant: int) -> int:
        """Returns the same instant since there are no transitions."""
        return instant
    
    def previous_transition(self, instant: int) -> int:
        """Returns the same instant since there are no transitions."""
        return instant
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, FixedDateTimeZone):
            return False
        return (self._id == other._id and 
                self._wall_offset == other._wall_offset and
                self._standard_offset == other._standard_offset)
    
    def __hash__(self) -> int:
        return super().__hash__()


# Initialize UTC constant
DateTimeZone.UTC = FixedDateTimeZone("UTC", "UTC", 0, 0)

# Initialize static fields
DateTimeZone._init_static()