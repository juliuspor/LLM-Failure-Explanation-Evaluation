def _update_bounds(self, period: TimePeriod, index: int) -> None:
    def _millis_from_period(p: TimePeriod) -> int:
        if p is None:
            raise ValueError("Null period encountered when computing milliseconds.")
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis(), p.get_end_millis()
        # For generic TimePeriod, expect get_start/get_end to return datetime-like
        start_obj = p.get_start()
        end_obj = p.get_end()
        try:
            start_ms = int(start_obj.timestamp() * 1000)
            end_ms = int(end_obj.timestamp() * 1000)
        except Exception:
            # If start/end are already integers (milliseconds), coerce
            try:
                start_ms = int(start_obj)
                end_ms = int(end_obj)
            except Exception:
                raise TypeError("Unable to convert period start/end to milliseconds")
        return start_ms, end_ms

    # Normalize start/end to integer milliseconds
    start, end = _millis_from_period(period)
    # compute middle as integer milliseconds
    middle = start + ((end - start) // 2)

    # Helper to safely get period at an index and its millis
    def _get_period_millis_at(idx: int):
        if idx < 0 or idx >= len(self._data):
            return None
        p = self.get_data_item(idx).get_period()
        return _millis_from_period(p)

    # min start
    if 0 <= self._min_start_index < len(self._data):
        ms_start, _ = _get_period_millis_at(self._min_start_index)
        if start < ms_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if 0 <= self._max_start_index < len(self._data):
        ms_start, _ = _get_period_millis_at(self._max_start_index)
        if start > ms_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if 0 <= self._min_middle_index < len(self._data):
        s, e = _get_period_millis_at(self._min_middle_index)
        min_middle = s + ((e - s) // 2)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if 0 <= self._max_middle_index < len(self._data):
        s, e = _get_period_millis_at(self._max_middle_index)
        max_middle = s + ((e - s) // 2)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if 0 <= self._min_end_index < len(self._data):
        _, min_end = _get_period_millis_at(self._min_end_index)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if 0 <= self._max_end_index < len(self._data):
        _, max_end = _get_period_millis_at(self._max_end_index)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index
