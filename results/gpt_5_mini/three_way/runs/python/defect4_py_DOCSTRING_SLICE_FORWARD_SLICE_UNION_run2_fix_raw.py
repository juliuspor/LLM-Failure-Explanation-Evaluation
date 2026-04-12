def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds for the new period
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # Helper to get start, end, middle for a period at given index
    def _get_period_times(idx: int):
        p = self.get_data_item(idx).get_period()
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        m = s + ((e - s) // 2)
        return s, e, m

    # min start
    if self._min_start_index >= 0:
        min_start, _, _ = _get_period_times(self._min_start_index)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0:
        max_start, _, _ = _get_period_times(self._max_start_index)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0:
        _, _, min_middle = _get_period_times(self._min_middle_index)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0:
        _, _, max_middle = _get_period_times(self._max_middle_index)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0:
        _, min_end, _ = _get_period_times(self._min_end_index)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0:
        _, max_end, _ = _get_period_times(self._max_end_index)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index
