def _update_bounds(self, period: TimePeriod, index: int) -> None:
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    middle = start + ((end - start) // 2)
    min_start_idx = getattr(self, "_min_start_index", -1)
    if min_start_idx >= 0:
        min_start_period = self.get_data_item(min_start_idx).get_period()
        if isinstance(min_start_period, SimpleTimePeriod):
            min_start = min_start_period.get_start_millis()
        else:
            min_start = int(min_start_period.get_start().timestamp() * 1000)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    max_start_idx = getattr(self, "_max_start_index", -1)
    if max_start_idx >= 0:
        max_start_period = self.get_data_item(max_start_idx).get_period()
        if isinstance(max_start_period, SimpleTimePeriod):
            max_start = max_start_period.get_start_millis()
        else:
            max_start = int(max_start_period.get_start().timestamp() * 1000)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    min_middle_idx = getattr(self, "_min_middle_index", -1)
    if min_middle_idx >= 0:
        min_middle_period = self.get_data_item(min_middle_idx).get_period()
        if isinstance(min_middle_period, SimpleTimePeriod):
            s = min_middle_period.get_start_millis()
            e = min_middle_period.get_end_millis()
        else:
            s = int(min_middle_period.get_start().timestamp() * 1000)
            e = int(min_middle_period.get_end().timestamp() * 1000)
        min_middle = s + (e - s) // 2
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    max_middle_idx = getattr(self, "_max_middle_index", -1)
    if max_middle_idx >= 0:
        max_middle_period = self.get_data_item(max_middle_idx).get_period()
        if isinstance(max_middle_period, SimpleTimePeriod):
            s = max_middle_period.get_start_millis()
            e = max_middle_period.get_end_millis()
        else:
            s = int(max_middle_period.get_start().timestamp() * 1000)
            e = int(max_middle_period.get_end().timestamp() * 1000)
        max_middle = s + (e - s) // 2
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    min_end_idx = getattr(self, "_min_end_index", -1)
    if min_end_idx >= 0:
        min_end_period = self.get_data_item(min_end_idx).get_period()
        if isinstance(min_end_period, SimpleTimePeriod):
            min_end = min_end_period.get_end_millis()
        else:
            min_end = int(min_end_period.get_end().timestamp() * 1000)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    max_end_idx = getattr(self, "_max_end_index", -1)
    if max_end_idx >= 0:
        max_end_period = self.get_data_item(max_end_idx).get_period()
        if isinstance(max_end_period, SimpleTimePeriod):
            max_end = max_end_period.get_end_millis()
        else:
            max_end = int(max_end_period.get_end().timestamp() * 1000)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index