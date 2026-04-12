def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # helper to get start/end/middle millis for a period at a given index
    def _get_start_at(idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)

    def _get_end_at(idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)

    def _get_middle_at(idx: int) -> int:
        s = _get_start_at(idx)
        e = _get_end_at(idx)
        return s + ((e - s) // 2)

    # min start
    if self._min_start_index < 0:
        self._min_start_index = index
    else:
        min_start = _get_start_at(self._min_start_index)
        if start < min_start:
            self._min_start_index = index

    # max start
    if self._max_start_index < 0:
        self._max_start_index = index
    else:
        max_start = _get_start_at(self._max_start_index)
        if start > max_start:
            self._max_start_index = index

    # min middle
    if self._min_middle_index < 0:
        self._min_middle_index = index
    else:
        min_middle = _get_middle_at(self._min_middle_index)
        if middle < min_middle:
            self._min_middle_index = index

    # max middle
    if self._max_middle_index < 0:
        self._max_middle_index = index
    else:
        max_middle = _get_middle_at(self._max_middle_index)
        if middle > max_middle:
            self._max_middle_index = index

    # min end
    if self._min_end_index < 0:
        self._min_end_index = index
    else:
        min_end = _get_end_at(self._min_end_index)
        if end < min_end:
            self._min_end_index = index

    # max end
    if self._max_end_index < 0:
        self._max_end_index = index
    else:
        max_end = _get_end_at(self._max_end_index)
        if end > max_end:
            self._max_end_index = index