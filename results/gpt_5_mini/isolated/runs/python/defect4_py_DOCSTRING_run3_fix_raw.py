def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # compute start/end in milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # ensure timestamp tracking attributes exist on the instance
    # these will store the actual timestamp values (milliseconds)
    if not hasattr(self, '_min_start_timestamp'):
        self._min_start_timestamp = None
        self._max_start_timestamp = None
        self._min_middle_timestamp = None
        self._max_middle_timestamp = None
        self._min_end_timestamp = None
        self._max_end_timestamp = None

    # min start
    if self._min_start_index >= 0 and self._min_start_timestamp is not None:
        if start < self._min_start_timestamp:
            self._min_start_timestamp = start
            self._min_start_index = index
    else:
        self._min_start_timestamp = start
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0 and self._max_start_timestamp is not None:
        if start > self._max_start_timestamp:
            self._max_start_timestamp = start
            self._max_start_index = index
    else:
        self._max_start_timestamp = start
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0 and self._min_middle_timestamp is not None:
        if middle < self._min_middle_timestamp:
            self._min_middle_timestamp = middle
            self._min_middle_index = index
    else:
        self._min_middle_timestamp = middle
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0 and self._max_middle_timestamp is not None:
        if middle > self._max_middle_timestamp:
            self._max_middle_timestamp = middle
            self._max_middle_index = index
    else:
        self._max_middle_timestamp = middle
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0 and self._min_end_timestamp is not None:
        if end < self._min_end_timestamp:
            self._min_end_timestamp = end
            self._min_end_index = index
    else:
        self._min_end_timestamp = end
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0 and self._max_end_timestamp is not None:
        if end > self._max_end_timestamp:
            self._max_end_timestamp = end
            self._max_end_index = index
    else:
        self._max_end_timestamp = end
        self._max_end_index = index