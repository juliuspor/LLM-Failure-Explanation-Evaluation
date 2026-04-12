def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    
    middle = start + ((end - start) // 2)

    def get_start_millis(p):
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)

    def get_end_millis(p):
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)

    def get_middle_millis(p):
        s = get_start_millis(p)
        e = get_end_millis(p)
        return s + (e - s) // 2

    # Update min/max start
    if self._min_start_index < 0:
        self._min_start_index = index
    else:
        min_start = get_start_millis(self.get_data_item(self._min_start_index).get_period())
        if start < min_start:
            self._min_start_index = index

    if self._max_start_index < 0:
        self._max_start_index = index
    else:
        max_start = get_start_millis(self.get_data_item(self._max_start_index).get_period())
        if start > max_start:
            self._max_start_index = index

    # Update min/max middle
    if self._min_middle_index < 0:
        self._min_middle_index = index
    else:
        min_middle = get_middle_millis(self.get_data_item(self._min_middle_index).get_period())
        if middle < min_middle:
            self._min_middle_index = index

    if self._max_middle_index < 0:
        self._max_middle_index = index
    else:
        max_middle = get_middle_millis(self.get_data_item(self._max_middle_index).get_period())
        if middle > max_middle:
            self._max_middle_index = index

    # Update min/max end
    if self._min_end_index < 0:
        self._min_end_index = index
    else:
        min_end = get_end_millis(self.get_data_item(self._min_end_index).get_period())
        if end < min_end:
            self._min_end_index = index

    if self._max_end_index < 0:
        self._max_end_index = index
    else:
        max_end = get_end_millis(self.get_data_item(self._max_end_index).get_period())
        if end > max_end:
            self._max_end_index = index