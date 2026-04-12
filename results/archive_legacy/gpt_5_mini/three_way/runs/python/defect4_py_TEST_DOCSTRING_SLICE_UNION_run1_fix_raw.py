def _update_bounds(self, period: TimePeriod, index: int) -> None:
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    middle = start + ((end - start) // 2)
    if self._min_start_index >= 0:
        existing = self.get_data_item(self._min_start_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            exist_start = existing.get_start_millis()
        else:
            exist_start = int(existing.get_start().timestamp() * 1000)
        if start < exist_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        existing = self.get_data_item(self._max_start_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            exist_start = existing.get_start_millis()
        else:
            exist_start = int(existing.get_start().timestamp() * 1000)
        if start > exist_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        existing = self.get_data_item(self._min_middle_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            es = existing.get_start_millis()
            ee = existing.get_end_millis()
        else:
            es = int(existing.get_start().timestamp() * 1000)
            ee = int(existing.get_end().timestamp() * 1000)
        exist_middle = es + ((ee - es) // 2)
        if middle < exist_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        existing = self.get_data_item(self._max_middle_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            es = existing.get_start_millis()
            ee = existing.get_end_millis()
        else:
            es = int(existing.get_start().timestamp() * 1000)
            ee = int(existing.get_end().timestamp() * 1000)
        exist_middle = es + ((ee - es) // 2)
        if middle > exist_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        existing = self.get_data_item(self._min_end_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            exist_end = existing.get_end_millis()
        else:
            exist_end = int(existing.get_end().timestamp() * 1000)
        if end < exist_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        existing = self.get_data_item(self._max_end_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            exist_end = existing.get_end_millis()
        else:
            exist_end = int(existing.get_end().timestamp() * 1000)
        if end > exist_end:
            self._max_end_index = index
    else:
        self._max_end_index = index
