def _update_bounds(self, period: TimePeriod, index: int) -> None:
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    middle = start + ((end - start) // 2)
    def period_start_ms_at(idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)
    def period_end_ms_at(idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)
    def period_middle_ms_at(idx: int) -> int:
        s = period_start_ms_at(idx)
        e = period_end_ms_at(idx)
        return s + ((e - s) // 2)
    if self._min_start_index >= 0:
        min_start = period_start_ms_at(self._min_start_index)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        max_start = period_start_ms_at(self._max_start_index)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        min_middle = period_middle_ms_at(self._min_middle_index)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        max_middle = period_middle_ms_at(self._max_middle_index)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        min_end = period_end_ms_at(self._min_end_index)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        max_end = period_end_ms_at(self._max_end_index)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index