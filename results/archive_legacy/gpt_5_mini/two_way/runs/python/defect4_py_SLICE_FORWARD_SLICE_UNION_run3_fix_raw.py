def _update_bounds(self, period: TimePeriod, index: int) -> None:
    def millis_for_period(p: TimePeriod):
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        m = s + ((e - s) // 2)
        return s, e, m
    start, end, middle = millis_for_period(period)
    if self._min_start_index >= 0:
        min_start_period = self.get_data_item(self._min_start_index).get_period()
        min_start, _, _ = millis_for_period(min_start_period)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        max_start_period = self.get_data_item(self._max_start_index).get_period()
        max_start, _, _ = millis_for_period(max_start_period)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        min_middle_period = self.get_data_item(self._min_middle_index).get_period()
        _, _, min_middle = millis_for_period(min_middle_period)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        max_middle_period = self.get_data_item(self._max_middle_index).get_period()
        _, _, max_middle = millis_for_period(max_middle_period)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        min_end_period = self.get_data_item(self._min_end_index).get_period()
        _, min_end, _ = millis_for_period(min_end_period)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        max_end_period = self.get_data_item(self._max_end_index).get_period()
        _, max_end, _ = millis_for_period(max_end_period)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index