def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Helper to get start/end millis
    def get_start_millis(p: TimePeriod) -> int:
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)

    def get_end_millis(p: TimePeriod) -> int:
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)

    start = get_start_millis(period)
    end = get_end_millis(period)
    middle = start + ((end - start) // 2)

    # min start
    if self._min_start_index >= 0:
        min_start_period = self.get_data_item(self._min_start_index).get_period()
        min_start = get_start_millis(min_start_period)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0:
        max_start_period = self.get_data_item(self._max_start_index).get_period()
        max_start = get_start_millis(max_start_period)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0:
        min_middle_period = self.get_data_item(self._min_middle_index).get_period()
        s = get_start_millis(min_middle_period)
        e = get_end_millis(min_middle_period)
        min_middle = s + ((e - s) // 2)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0:
        max_middle_period = self.get_data_item(self._max_middle_index).get_period()
        s = get_start_millis(max_middle_period)
        e = get_end_millis(max_middle_period)
        max_middle = s + ((e - s) // 2)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0:
        min_end_period = self.get_data_item(self._min_end_index).get_period()
        min_end = get_end_millis(min_end_period)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0:
        max_end_period = self.get_data_item(self._max_end_index).get_period()
        max_end = get_end_millis(max_end_period)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index