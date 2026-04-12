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
            comp = p.get_start_millis()
        else:
            comp = int(p.get_start().timestamp() * 1000)
        if start < comp:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        p = self.get_data_item(self._max_start_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            comp = p.get_start_millis()
        else:
            comp = int(p.get_start().timestamp() * 1000)
        if start > comp:
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
        comp = s + ((e - s) // 2)
        if middle < comp:
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
        comp = s + ((e - s) // 2)
        if middle > comp:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        p = self.get_data_item(self._min_end_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            comp = p.get_end_millis()
        else:
            comp = int(p.get_end().timestamp() * 1000)
        if end < comp:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        p = self.get_data_item(self._max_end_index).get_period()
        if isinstance(p, SimpleTimePeriod):
            comp = p.get_end_millis()
        else:
            comp = int(p.get_end().timestamp() * 1000)
        if end > comp:
            self._max_end_index = index
    else:
        self._max_end_index = index