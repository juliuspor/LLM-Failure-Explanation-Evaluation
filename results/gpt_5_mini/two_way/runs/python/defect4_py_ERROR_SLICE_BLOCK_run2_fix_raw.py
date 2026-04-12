def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    n = len(self._data)
    # Helper to validate an index
    def valid(idx: int) -> bool:
        return 0 <= idx < n

    # Update min start
    if valid(self._min_start_index):
        min_start_period = self.get_data_item(self._min_start_index).get_period()
        if isinstance(min_start_period, SimpleTimePeriod):
            min_start = min_start_period.get_start_millis()
        else:
            min_start = int(min_start_period.get_start().timestamp() * 1000)
        if start < min_start:
            self._min_start_index = index
    else:
        # Initialize to the new index if no valid current index
        self._min_start_index = index

    # Update max start
    if valid(self._max_start_index):
        max_start_period = self.get_data_item(self._max_start_index).get_period()
        if isinstance(max_start_period, SimpleTimePeriod):
            max_start = max_start_period.get_start_millis()
        else:
            max_start = int(max_start_period.get_start().timestamp() * 1000)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # Update min middle
    if valid(self._min_middle_index):
        min_middle_period = self.get_data_item(self._min_middle_index).get_period()
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

    # Update max middle (fixed bug: previously used _min_middle_index accidentally)
    if valid(self._max_middle_index):
        max_middle_period = self.get_data_item(self._max_middle_index).get_period()
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

    # Update min end
    if valid(self._min_end_index):
        min_end_period = self.get_data_item(self._min_end_index).get_period()
        if isinstance(min_end_period, SimpleTimePeriod):
            min_end = min_end_period.get_end_millis()
        else:
            min_end = int(min_end_period.get_end().timestamp() * 1000)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # Update max end
    if valid(self._max_end_index):
        max_end_period = self.get_data_item(self._max_end_index).get_period()
        if isinstance(max_end_period, SimpleTimePeriod):
            max_end = max_end_period.get_end_millis()
        else:
            max_end = int(max_end_period.get_end().timestamp() * 1000)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index

    # Safety: if any index became invalid due to external mutations, recalculate
    # (this keeps invariants safe in face of other list operations)
    if not all((valid(self._min_start_index), valid(self._max_start_index),
                valid(self._min_middle_index), valid(self._max_middle_index),
                valid(self._min_end_index), valid(self._max_end_index))):
        # Recalculate fully to ensure consistency
        self._recalculate_bounds()