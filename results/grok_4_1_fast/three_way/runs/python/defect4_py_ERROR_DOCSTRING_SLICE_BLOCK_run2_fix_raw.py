def _update_bounds(self, period: TimePeriod, index: int) -> None:
    def get_millis(p: TimePeriod) -> tuple[int, int]:
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis(), p.get_end_millis()
        else:
            start_ms = int(p.get_start().timestamp() * 1000)
            end_ms = int(p.get_end().timestamp() * 1000)
            return start_ms, end_ms
    
    start, end = get_millis(period)
    middle = start + ((end - start) // 2)
    
    if self._min_start_index >= 0:
        min_start_period = self.get_data_item(self._min_start_index).get_period()
        min_start, _ = get_millis(min_start_period)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index
    
    if self._max_start_index >= 0:
        max_start_period = self.get_data_item(self._max_start_index).get_period()
        max_start, _ = get_millis(max_start_period)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index
    
    if self._min_middle_index >= 0:
        min_middle_period = self.get_data_item(self._min_middle_index).get_period()
        s, e = get_millis(min_middle_period)
        min_middle = s + (e - s) // 2
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    
    if self._max_middle_index >= 0:
        max_middle_period = self.get_data_item(self._max_middle_index).get_period()
        s, e = get_millis(max_middle_period)
        max_middle = s + (e - s) // 2
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    
    if self._min_end_index >= 0:
        min_end_period = self.get_data_item(self._min_end_index).get_period()
        _, min_end = get_millis(min_end_period)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index
    
    if self._max_end_index >= 0:
        max_end_period = self.get_data_item(self._max_end_index).get_period()
        _, max_end = get_millis(max_end_period)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index