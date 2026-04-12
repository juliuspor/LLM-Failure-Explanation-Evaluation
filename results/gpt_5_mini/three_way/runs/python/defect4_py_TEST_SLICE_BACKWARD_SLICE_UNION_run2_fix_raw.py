def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # min start
    if self._min_start_index >= 0:
        stored = self.get_data_item(self._min_start_index).get_period()
        if isinstance(stored, SimpleTimePeriod):
            stored_start = stored.get_start_millis()
        else:
            stored_start = int(stored.get_start().timestamp() * 1000)
        if start < stored_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0:
        stored = self.get_data_item(self._max_start_index).get_period()
        if isinstance(stored, SimpleTimePeriod):
            stored_start = stored.get_start_millis()
        else:
            stored_start = int(stored.get_start().timestamp() * 1000)
        if start > stored_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0:
        stored = self.get_data_item(self._min_middle_index).get_period()
        if isinstance(stored, SimpleTimePeriod):
            s = stored.get_start_millis()
            e = stored.get_end_millis()
        else:
            s = int(stored.get_start().timestamp() * 1000)
            e = int(stored.get_end().timestamp() * 1000)
        stored_middle = s + (e - s) // 2
        if middle < stored_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0:
        stored = self.get_data_item(self._max_middle_index).get_period()
        if isinstance(stored, SimpleTimePeriod):
            s = stored.get_start_millis()
            e = stored.get_end_millis()
        else:
            s = int(stored.get_start().timestamp() * 1000)
            e = int(stored.get_end().timestamp() * 1000)
        stored_middle = s + (e - s) // 2
        if middle > stored_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0:
        stored = self.get_data_item(self._min_end_index).get_period()
        if isinstance(stored, SimpleTimePeriod):
            stored_end = stored.get_end_millis()
        else:
            stored_end = int(stored.get_end().timestamp() * 1000)
        if end < stored_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0:
        stored = self.get_data_item(self._max_end_index).get_period()
        if isinstance(stored, SimpleTimePeriod):
            stored_end = stored.get_end_millis()
        else:
            stored_end = int(stored.get_end().timestamp() * 1000)
        if end > stored_end:
            self._max_end_index = index
    else:
        self._max_end_index = index
