def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)
    data_len = len(self._data)

    # Helper to safely get start/end/middle for a stored index
    def _start_at(idx: int) -> int:
        tp = self.get_data_item(idx).get_period()
        if isinstance(tp, SimpleTimePeriod):
            return tp.get_start_millis()
        return int(tp.get_start().timestamp() * 1000)

    def _end_at(idx: int) -> int:
        tp = self.get_data_item(idx).get_period()
        if isinstance(tp, SimpleTimePeriod):
            return tp.get_end_millis()
        return int(tp.get_end().timestamp() * 1000)

    def _middle_at(idx: int) -> int:
        s = _start_at(idx)
        e = _end_at(idx)
        return s + ((e - s) // 2)

    # min start
    if 0 <= self._min_start_index < data_len:
        try:
            min_start = _start_at(self._min_start_index)
        except Exception:
            min_start = None
        if min_start is None or start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if 0 <= self._max_start_index < data_len:
        try:
            max_start = _start_at(self._max_start_index)
        except Exception:
            max_start = None
        if max_start is None or start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if 0 <= self._min_middle_index < data_len:
        try:
            min_middle = _middle_at(self._min_middle_index)
        except Exception:
            min_middle = None
        if min_middle is None or middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if 0 <= self._max_middle_index < data_len:
        try:
            max_middle = _middle_at(self._max_middle_index)
        except Exception:
            max_middle = None
        if max_middle is None or middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if 0 <= self._min_end_index < data_len:
        try:
            min_end = _end_at(self._min_end_index)
        except Exception:
            min_end = None
        if min_end is None or end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if 0 <= self._max_end_index < data_len:
        try:
            max_end = _end_at(self._max_end_index)
        except Exception:
            max_end = None
        if max_end is None or end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index