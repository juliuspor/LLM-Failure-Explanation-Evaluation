def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds for the new period
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # Update min start
    if self._min_start_index < 0:
        self._min_start_index = index
    else:
        ref = self.get_data_item(self._min_start_index).get_period()
        if isinstance(ref, SimpleTimePeriod):
            ref_start = ref.get_start_millis()
        else:
            ref_start = int(ref.get_start().timestamp() * 1000)
        if start < ref_start:
            self._min_start_index = index

    # Update max start
    if self._max_start_index < 0:
        self._max_start_index = index
    else:
        ref = self.get_data_item(self._max_start_index).get_period()
        if isinstance(ref, SimpleTimePeriod):
            ref_start = ref.get_start_millis()
        else:
            ref_start = int(ref.get_start().timestamp() * 1000)
        if start > ref_start:
            self._max_start_index = index

    # Update min middle
    if self._min_middle_index < 0:
        self._min_middle_index = index
    else:
        ref = self.get_data_item(self._min_middle_index).get_period()
        if isinstance(ref, SimpleTimePeriod):
            s = ref.get_start_millis()
            e = ref.get_end_millis()
        else:
            s = int(ref.get_start().timestamp() * 1000)
            e = int(ref.get_end().timestamp() * 1000)
        ref_middle = s + ((e - s) // 2)
        if middle < ref_middle:
            self._min_middle_index = index

    # Update max middle
    if self._max_middle_index < 0:
        self._max_middle_index = index
    else:
        ref = self.get_data_item(self._max_middle_index).get_period()
        if isinstance(ref, SimpleTimePeriod):
            s = ref.get_start_millis()
            e = ref.get_end_millis()
        else:
            s = int(ref.get_start().timestamp() * 1000)
            e = int(ref.get_end().timestamp() * 1000)
        ref_middle = s + ((e - s) // 2)
        if middle > ref_middle:
            self._max_middle_index = index

    # Update min end
    if self._min_end_index < 0:
        self._min_end_index = index
    else:
        ref = self.get_data_item(self._min_end_index).get_period()
        if isinstance(ref, SimpleTimePeriod):
            ref_end = ref.get_end_millis()
        else:
            ref_end = int(ref.get_end().timestamp() * 1000)
        if end < ref_end:
            self._min_end_index = index

    # Update max end
    if self._max_end_index < 0:
        self._max_end_index = index
    else:
        ref = self.get_data_item(self._max_end_index).get_period()
        if isinstance(ref, SimpleTimePeriod):
            ref_end = ref.get_end_millis()
        else:
            ref_end = int(ref.get_end().timestamp() * 1000)
        if end > ref_end:
            self._max_end_index = index