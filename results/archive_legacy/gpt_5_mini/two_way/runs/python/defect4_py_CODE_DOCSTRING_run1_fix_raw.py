def _update_bounds(self, period: TimePeriod, index: int) -> None:
    def millis_start(p: TimePeriod) -> int:
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)
    def millis_end(p: TimePeriod) -> int:
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    middle = start + ((end - start) // 2)
    if self._min_start_index >= 0:
        min_start_period = self.get_data_item(self._min_start_index).get_period()
        min_start = millis_start(min_start_period)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        max_start_period = self.get_data_item(self._max_start_index).get_period()
        max_start = millis_start(max_start_period)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        min_middle_period = self.get_data_item(self._min_middle_index).get_period()
        s = millis_start(min_middle_period)
        e = millis_end(min_middle_period)
        min_middle = s + (e - s) // 2
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        max_middle_period = self.get_data_item(self._max_middle_index).get_period()
        s = millis_start(max_middle_period)
        e = millis_end(max_middle_period)
        max_middle = s + (e - s) // 2
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        min_end_period = self.get_data_item(self._min_end_index).get_period()
        min_end = millis_end(min_end_period)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        max_end_period = self.get_data_item(self._max_end_index).get_period()
        max_end = millis_end(max_end_period)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index