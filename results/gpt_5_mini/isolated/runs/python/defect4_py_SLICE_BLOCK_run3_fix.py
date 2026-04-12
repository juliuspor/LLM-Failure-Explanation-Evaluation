# -*- coding: utf-8 -*-
"""
TimePeriodValues - A structure containing time period value instances.
"""

from typing import List, Optional, Any, Callable
from datetime import datetime
import copy


class SeriesException(Exception):
    """Exception raised for series-related errors."""
    pass


class SeriesChangeEvent:
    """Event indicating a series has changed."""
    
    def __init__(self, source: 'Series'):
        self._source = source
    
    @property
    def source(self) -> 'Series':
        return self._source


class Series:
    """
    Base class for data series.
    """
    
    def __init__(self, key: Any, description: str = None):
        """
        Creates a new series.
        
        Args:
            key: the series key (not None)
            description: the series description (None permitted)
        """
        if key is None:
            raise ValueError("The 'key' argument cannot be None.")
        self._key = key
        self._description = description
        self._listeners: List[Callable[[SeriesChangeEvent], None]] = []
        self._property_change_listeners: List[Callable[[str, Any, Any], None]] = []
        self._notify = True
    
    @property
    def key(self) -> Any:
        """Returns the key for the series."""
        return self._key
    
    def get_key(self) -> Any:
        """Returns the key for the series."""
        return self._key
    
    @property
    def description(self) -> Optional[str]:
        """Returns the description of the series."""
        return self._description
    
    def get_description(self) -> Optional[str]:
        """Returns the description of the series."""
        return self._description
    
    def set_description(self, description: str) -> None:
        """Sets the description of the series."""
        self._description = description
    
    def get_notify(self) -> bool:
        """Returns the notify flag."""
        return self._notify
    
    def set_notify(self, notify: bool) -> None:
        """Sets the notify flag."""
        self._notify = notify
    
    def add_change_listener(self, listener: Callable[[SeriesChangeEvent], None]) -> None:
        """Adds a change listener."""
        self._listeners.append(listener)
    
    def remove_change_listener(self, listener: Callable[[SeriesChangeEvent], None]) -> None:
        """Removes a change listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def fire_series_changed(self) -> None:
        """Fires a series changed event."""
        if self._notify:
            event = SeriesChangeEvent(self)
            for listener in self._listeners:
                listener(event)
    
    def fire_property_change(self, name: str, old_value: Any, new_value: Any) -> None:
        """Fires a property change event."""
        for listener in self._property_change_listeners:
            listener(name, old_value, new_value)
    
    def __eq__(self, other) -> bool:
        if other is self:
            return True
        if not isinstance(other, Series):
            return False
        if self._key != other._key:
            return False
        if self._description != other._description:
            return False
        return True
    
    def __hash__(self) -> int:
        return hash((self._key, self._description))


class TimePeriod:
    """
    Represents a time period with a start and end time.
    """
    
    def get_start(self) -> datetime:
        """Returns the start time."""
        raise NotImplementedError
    
    def get_end(self) -> datetime:
        """Returns the end time."""
        raise NotImplementedError


class SimpleTimePeriod(TimePeriod):
    """
    A simple time period with explicit start and end times.
    """
    
    def __init__(self, start: int, end: int):
        """
        Creates a new time period.
        
        Args:
            start: the start time in milliseconds
            end: the end time in milliseconds
        """
        if start > end:
            raise ValueError("Start time must be <= end time.")
        self._start = start
        self._end = end
    
    def get_start(self) -> datetime:
        """Returns the start time as a datetime."""
        return datetime.fromtimestamp(self._start / 1000.0)
    
    def get_end(self) -> datetime:
        """Returns the end time as a datetime."""
        return datetime.fromtimestamp(self._end / 1000.0)
    
    def get_start_millis(self) -> int:
        """Returns the start time in milliseconds."""
        return self._start
    
    def get_end_millis(self) -> int:
        """Returns the end time in milliseconds."""
        return self._end
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, SimpleTimePeriod):
            return False
        return self._start == other._start and self._end == other._end
    
    def __hash__(self) -> int:
        return hash((self._start, self._end))
    
    def clone(self) -> 'SimpleTimePeriod':
        """Returns a clone of this time period."""
        return SimpleTimePeriod(self._start, self._end)


class TimePeriodValue:
    """
    A value associated with a time period.
    """
    
    def __init__(self, period: TimePeriod, value: float = None):
        """
        Creates a new time period value.
        
        Args:
            period: the time period (not None)
            value: the value (None permitted)
        """
        if period is None:
            raise ValueError("Null 'period' argument.")
        self._period = period
        self._value = value
    
    def get_period(self) -> TimePeriod:
        """Returns the time period."""
        return self._period
    
    def get_value(self) -> Optional[float]:
        """Returns the value."""
        return self._value
    
    def set_value(self, value: float) -> None:
        """Sets the value."""
        self._value = value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TimePeriodValue):
            return False
        if self._period != other._period:
            return False
        if self._value != other._value:
            return False
        return True
    
    def __hash__(self) -> int:
        return hash((self._period, self._value))
    
    def clone(self) -> 'TimePeriodValue':
        """Returns a clone of this time period value."""
        return TimePeriodValue(self._period, self._value)


class TimePeriodValues(Series):
    """
    A structure containing zero, one or many TimePeriodValue instances.
    The time periods can overlap, and are maintained in the order that they are
    added to the collection.
    
    This is similar to the TimeSeries class, except that the time
    periods can have irregular lengths.
    """
    
    # Default value for the domain description.
    DEFAULT_DOMAIN_DESCRIPTION = "Time"
    
    # Default value for the range description.
    DEFAULT_RANGE_DESCRIPTION = "Value"
    
    def __init__(self, name: Any, domain: str = None, range_desc: str = None):
        """
        Creates a new (empty) collection of time period values.
        
        Args:
            name: the name of the series (not None)
            domain: the domain description
            range_desc: the range description
        """
        super().__init__(name)
        self._domain = domain if domain is not None else self.DEFAULT_DOMAIN_DESCRIPTION
        self._range = range_desc if range_desc is not None else self.DEFAULT_RANGE_DESCRIPTION
        self._data: List[TimePeriodValue] = []
        
        # Index of the time period with the minimum start milliseconds.
        self._min_start_index = -1
        # Index of the time period with the maximum start milliseconds.
        self._max_start_index = -1
        # Index of the time period with the minimum middle milliseconds.
        self._min_middle_index = -1
        # Index of the time period with the maximum middle milliseconds.
        self._max_middle_index = -1
        # Index of the time period with the minimum end milliseconds.
        self._min_end_index = -1
        # Index of the time period with the maximum end milliseconds.
        self._max_end_index = -1
    
    def get_domain_description(self) -> str:
        """Returns the domain description."""
        return self._domain
    
    def set_domain_description(self, description: str) -> None:
        """Sets the domain description."""
        old = self._domain
        self._domain = description
        self.fire_property_change("Domain", old, description)
    
    def get_range_description(self) -> str:
        """Returns the range description."""
        return self._range
    
    def set_range_description(self, description: str) -> None:
        """Sets the range description."""
        old = self._range
        self._range = description
        self.fire_property_change("Range", old, description)
    
    def get_item_count(self) -> int:
        """Returns the number of items in the series."""
        return len(self._data)
    
    def get_data_item(self, index: int) -> TimePeriodValue:
        """Returns one data item for the series."""
        return self._data[index]
    
    def get_time_period(self, index: int) -> TimePeriod:
        """Returns the time period at the specified index."""
        return self.get_data_item(index).get_period()
    
    def get_value(self, index: int) -> Optional[float]:
        """Returns the value at the specified index."""
        return self.get_data_item(index).get_value()
    
    def add(self, item_or_period, value: float = None) -> None:
        """
        Adds a data item to the series.
        
        Args:
            item_or_period: TimePeriodValue or TimePeriod
            value: the value (only if item_or_period is a TimePeriod)
        """
        if isinstance(item_or_period, TimePeriodValue):
            item = item_or_period
        else:
            # Assume it's a TimePeriod
            item = TimePeriodValue(item_or_period, value)
        
        if item is None:
            raise ValueError("Null item not allowed.")
        
        self._data.append(item)
        self._update_bounds(item.get_period(), len(self._data) - 1)
        self.fire_series_changed()
    
    def _update_bounds(self, period: TimePeriod, index: int) -> None:
        # Get start and end as milliseconds
        if isinstance(period, SimpleTimePeriod):
            start = period.get_start_millis()
            end = period.get_end_millis()
        else:
            start = int(period.get_start().timestamp() * 1000)
            end = int(period.get_end().timestamp() * 1000)

        middle = start + ((end - start) // 2)

        # Use getattr to provide defaults in case attributes missing
        min_start_idx = getattr(self, '_min_start_index', -1)
        if min_start_idx >= 0:
            min_start_period = self.get_data_item(min_start_idx).get_period()
            if isinstance(min_start_period, SimpleTimePeriod):
                min_start = min_start_period.get_start_millis()
            else:
                min_start = int(min_start_period.get_start().timestamp() * 1000)
            if start < min_start:
                self._min_start_index = index
        else:
            self._min_start_index = index

        max_start_idx = getattr(self, '_max_start_index', -1)
        if max_start_idx >= 0:
            max_start_period = self.get_data_item(max_start_idx).get_period()
            if isinstance(max_start_period, SimpleTimePeriod):
                max_start = max_start_period.get_start_millis()
            else:
                max_start = int(max_start_period.get_start().timestamp() * 1000)
            if start > max_start:
                self._max_start_index = index
        else:
            self._max_start_index = index

        min_middle_idx = getattr(self, '_min_middle_index', -1)
        if min_middle_idx >= 0:
            min_middle_period = self.get_data_item(min_middle_idx).get_period()
            if isinstance(min_middle_period, SimpleTimePeriod):
                s = min_middle_period.get_start_millis()
                e = min_middle_period.get_end_millis()
            else:
                s = int(min_middle_period.get_start().timestamp() * 1000)
                e = int(min_middle_period.get_end().timestamp() * 1000)
            min_middle = s + (e - s) // 2
            if middle < min_middle:
                self._min_middle_index = index
        else:
            self._min_middle_index = index

        max_middle_idx = getattr(self, '_max_middle_index', -1)
        if max_middle_idx >= 0:
            max_middle_period = self.get_data_item(max_middle_idx).get_period()
            if isinstance(max_middle_period, SimpleTimePeriod):
                s = max_middle_period.get_start_millis()
                e = max_middle_period.get_end_millis()
            else:
                s = int(max_middle_period.get_start().timestamp() * 1000)
                e = int(max_middle_period.get_end().timestamp() * 1000)
            max_middle = s + (e - s) // 2
            if middle > max_middle:
                self._max_middle_index = index
        else:
            self._max_middle_index = index

        min_end_idx = getattr(self, '_min_end_index', -1)
        if min_end_idx >= 0:
            min_end_period = self.get_data_item(min_end_idx).get_period()
            if isinstance(min_end_period, SimpleTimePeriod):
                min_end = min_end_period.get_end_millis()
            else:
                min_end = int(min_end_period.get_end().timestamp() * 1000)
            if end < min_end:
                self._min_end_index = index
        else:
            self._min_end_index = index

        max_end_idx = getattr(self, '_max_end_index', -1)
        if max_end_idx >= 0:
            max_end_period = self.get_data_item(max_end_idx).get_period()
            if isinstance(max_end_period, SimpleTimePeriod):
                max_end = max_end_period.get_end_millis()
            else:
                max_end = int(max_end_period.get_end().timestamp() * 1000)
            if end > max_end:
                self._max_end_index = index
        else:
            self._max_end_index = index
    
    def _recalculate_bounds(self) -> None:
        """Recalculates the bounds for the collection of items."""
        self._min_start_index = -1
        self._min_middle_index = -1
        self._min_end_index = -1
        self._max_start_index = -1
        self._max_middle_index = -1
        self._max_end_index = -1
        for i in range(len(self._data)):
            tpv = self._data[i]
            self._update_bounds(tpv.get_period(), i)
    
    def update(self, index: int, value: float) -> None:
        """Updates the value of a data item."""
        item = self.get_data_item(index)
        item.set_value(value)
        self.fire_series_changed()
    
    def delete(self, start: int, end: int) -> None:
        """Deletes data from start until end index (end inclusive)."""
        for i in range(end - start + 1):
            del self._data[start]
        self._recalculate_bounds()
        self.fire_series_changed()
    
    def get_min_start_index(self) -> int:
        """Returns the index of the time period with the minimum start milliseconds."""
        return self._min_start_index
    
    def get_max_start_index(self) -> int:
        """Returns the index of the time period with the maximum start milliseconds."""
        return self._max_start_index
    
    def get_min_middle_index(self) -> int:
        """Returns the index of the time period with the minimum middle milliseconds."""
        return self._min_middle_index
    
    def get_max_middle_index(self) -> int:
        """Returns the index of the time period with the maximum middle milliseconds."""
        return self._max_middle_index
    
    def get_min_end_index(self) -> int:
        """Returns the index of the time period with the minimum end milliseconds."""
        return self._min_end_index
    
    def get_max_end_index(self) -> int:
        """Returns the index of the time period with the maximum end milliseconds."""
        return self._max_end_index
    
    def __eq__(self, other) -> bool:
        if other is self:
            return True
        if not isinstance(other, TimePeriodValues):
            return False
        if not super().__eq__(other):
            return False
        if self._domain != other._domain:
            return False
        if self._range != other._range:
            return False
        if len(self._data) != len(other._data):
            return False
        for i in range(len(self._data)):
            if self._data[i] != other._data[i]:
                return False
        return True
    
    def __hash__(self) -> int:
        result = hash(self._domain) if self._domain else 0
        result = 29 * result + (hash(self._range) if self._range else 0)
        result = 29 * result + hash(tuple(self._data))
        result = 29 * result + self._min_start_index
        result = 29 * result + self._max_start_index
        result = 29 * result + self._min_middle_index
        result = 29 * result + self._max_middle_index
        result = 29 * result + self._min_end_index
        result = 29 * result + self._max_end_index
        return result
    
    def clone(self) -> 'TimePeriodValues':
        """Returns a clone of the collection."""
        return self.create_copy(0, self.get_item_count() - 1)
    
    def create_copy(self, start: int, end: int) -> 'TimePeriodValues':
        """Creates a new instance by copying a subset of the data."""
        copy_obj = TimePeriodValues(self._key, self._domain, self._range)
        if len(self._data) > 0:
            for index in range(start, end + 1):
                item = self._data[index]
                clone_item = item.clone()
                try:
                    copy_obj.add(clone_item)
                except SeriesException:
                    print("Failed to add cloned item.")
        return copy_obj