def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # Ensure cached millisecond baselines exist on the object
    # Lazily create them if not present
    if not hasattr(self, '_min_start_millis'):
        self._min_start_millis = None
    if not hasattr(self, '_max_start_millis'):
        self._max_start_millis = None
    if not hasattr(self, '_min_middle_millis'):
        self._min_middle_millis = None
    if not hasattr(self, '_max_middle_millis'):
        self._max_middle_millis = None
    if not hasattr(self, '_min_end_millis'):
        self._min_end_millis = None
    if not hasattr(self, '_max_end_millis'):
        self._max_end_millis = None

    # min start
    if self._min_start_index >= 0 and self._min_start_millis is not None:
        if start < self._min_start_millis:
            self._min_start_index = index
            self._min_start_millis = start
    else:
        self._min_start_index = index
        self._min_start_millis = start

    # max start
    if self._max_start_index >= 0 and self._max_start_millis is not None:
        if start > self._max_start_millis:
            self._max_start_index = index
            self._max_start_millis = start
    else:
        self._max_start_index = index
        self._max_start_millis = start

    # min middle
    if self._min_middle_index >= 0 and self._min_middle_millis is not None:
        if middle < self._min_middle_millis:
            self._min_middle_index = index
            self._min_middle_millis = middle
    else:
        self._min_middle_index = index
        self._min_middle_millis = middle

    # max middle
    if self._max_middle_index >= 0 and self._max_middle_millis is not None:
        if middle > self._max_middle_millis:
            self._max_middle_index = index
            self._max_middle_millis = middle
    else:
        self._max_middle_index = index
        self._max_middle_millis = middle

    # min end
    if self._min_end_index >= 0 and self._min_end_millis is not None:
        if end < self._min_end_millis:
            self._min_end_index = index
            self._min_end_millis = end
    else:
        self._min_end_index = index
        self._min_end_millis = end

    # max end
    if self._max_end_index >= 0 and self._max_end_millis is not None:
        if end > self._max_end_millis:
            self._max_end_index = index
            self._max_end_millis = end
    else:
        self._max_end_index = index
        self._max_end_millis = end