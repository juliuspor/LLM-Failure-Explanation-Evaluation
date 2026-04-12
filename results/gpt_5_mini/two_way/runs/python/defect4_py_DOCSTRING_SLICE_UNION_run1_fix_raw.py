def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds for the new period
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # helper to extract start/end millis from an existing period
    def _get_start_end_millis(tp: TimePeriod):
        if isinstance(tp, SimpleTimePeriod):
            return tp.get_start_millis(), tp.get_end_millis()
        else:
            s = int(tp.get_start().timestamp() * 1000)
            e = int(tp.get_end().timestamp() * 1000)
            return s, e

    # min start
    if self._min_start_index >= 0:
        existing_period = self.get_data_item(self._min_start_index).get_period()
        min_start, _ = _get_start_end_millis(existing_period)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0:
        existing_period = self.get_data_item(self._max_start_index).get_period()
        max_start, _ = _get_start_end_millis(existing_period)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0:
        existing_period = self.get_data_item(self._min_middle_index).get_period()
        s, e = _get_start_end_millis(existing_period)
        min_middle = s + ((e - s) // 2)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0:
        existing_period = self.get_data_item(self._max_middle_index).get_period()
        s, e = _get_start_end_millis(existing_period)
        max_middle = s + ((e - s) // 2)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0:
        existing_period = self.get_data_item(self._min_end_index).get_period()
        _, min_end = _get_start_end_millis(existing_period)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0:
        existing_period = self.get_data_item(self._max_end_index).get_period()
        _, max_end = _get_start_end_millis(existing_period)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index