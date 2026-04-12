def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # MIN START
    if self._min_start_index >= 0:
        existing = self.get_data_item(self._min_start_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            existing_start = existing.get_start_millis()
        else:
            existing_start = int(existing.get_start().timestamp() * 1000)
        if start < existing_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # MAX START
    if self._max_start_index >= 0:
        existing = self.get_data_item(self._max_start_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            existing_start = existing.get_start_millis()
        else:
            existing_start = int(existing.get_start().timestamp() * 1000)
        if start > existing_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # MIN MIDDLE
    if self._min_middle_index >= 0:
        existing = self.get_data_item(self._min_middle_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            s = existing.get_start_millis()
            e = existing.get_end_millis()
        else:
            s = int(existing.get_start().timestamp() * 1000)
            e = int(existing.get_end().timestamp() * 1000)
        existing_middle = s + ((e - s) // 2)
        if middle < existing_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # MAX MIDDLE
    if self._max_middle_index >= 0:
        existing = self.get_data_item(self._max_middle_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            s = existing.get_start_millis()
            e = existing.get_end_millis()
        else:
            s = int(existing.get_start().timestamp() * 1000)
            e = int(existing.get_end().timestamp() * 1000)
        existing_middle = s + ((e - s) // 2)
        if middle > existing_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # MIN END
    if self._min_end_index >= 0:
        existing = self.get_data_item(self._min_end_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            existing_end = existing.get_end_millis()
        else:
            existing_end = int(existing.get_end().timestamp() * 1000)
        if end < existing_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # MAX END
    if self._max_end_index >= 0:
        existing = self.get_data_item(self._max_end_index).get_period()
        if isinstance(existing, SimpleTimePeriod):
            existing_end = existing.get_end_millis()
        else:
            existing_end = int(existing.get_end().timestamp() * 1000)
        if end > existing_end:
            self._max_end_index = index
    else:
        self._max_end_index = index