def _update_bounds(self, period: TimePeriod, index: int) -> None:
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    middle = start + ((end - start) // 2)
    if self._min_start_index >= 0:
        p = self.get_data_item(self._min_start_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            cur_min_start = p.get_start_millis()
        else:
            cur_min_start = int(p.get_start().timestamp() * 1000)
        if start < cur_min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        p = self.get_data_item(self._max_start_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            cur_max_start = p.get_start_millis()
        else:
            cur_max_start = int(p.get_start().timestamp() * 1000)
        if start > cur_max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        p = self.get_data_item(self._min_middle_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        cur_min_middle = s + ((e - s) // 2)
        if middle < cur_min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        p = self.get_data_item(self._max_middle_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        cur_max_middle = s + ((e - s) // 2)
        if middle > cur_max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        p = self.get_data_item(self._min_end_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            cur_min_end = p.get_end_millis()
        else:
            cur_min_end = int(p.get_end().timestamp() * 1000)
        if end < cur_min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        p = self.get_data_item(self._max_end_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            cur_max_end = p.get_end_millis()
        else:
            cur_max_end = int(p.get_end().timestamp() * 1000)
        if end > cur_max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index
