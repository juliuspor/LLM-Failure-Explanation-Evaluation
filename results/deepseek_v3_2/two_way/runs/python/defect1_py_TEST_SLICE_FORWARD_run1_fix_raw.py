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


class DateTimeZone(ABC):
    """Represents a time zone."""
    
    # Class variable for UTC instance
    UTC: 'DateTimeZone' = None
    
    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Returns a fixed offset time zone for the given hours and minutes.
        
        The sign of the hours and minutes components should match: either both
        negative or both non‑negative. If they have opposite signs, the total
        offset is computed as `hours * 60 + minutes` (respecting the sign of minutes).
        
        Args:
            hours: the offset hours, from -23 to