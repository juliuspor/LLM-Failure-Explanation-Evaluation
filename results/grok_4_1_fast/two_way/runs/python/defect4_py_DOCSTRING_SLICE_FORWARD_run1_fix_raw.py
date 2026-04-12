def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    
    middle = start + ((end - start) // 2)
    
    # Update min/max start
    if self._min_start_index < 0 or start < self._get_start_millis(self._min_start_index):
        self._min_start_index = index
    if self._max_start_index < 0 or start > self._get_start_millis(self._max_start_index):
        self._max_start_index = index
    
    # Update min/max middle
    if self._min_middle_index < 0 or middle < self._get_middle_millis(self._min_middle_index):
        self._min_middle_index = index
    if self._max_middle_index < 0 or middle > self._get_middle_millis(self._max_middle_index):
        self._max_middle_index = index
    
    # Update min/max end
    if self._min_end_index < 0 or end < self._get_end_millis(self._min_end_index):
        self._min_end_index = index
    if self._max_end_index < 0 or end > self._get_end_millis(self._max_end_index):
        self._max_end_index = index

    def _get_start_millis(self, idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        return p.get_start_millis() if isinstance(p, SimpleTimePeriod) else int(p.get_start().timestamp() * 1000)

    def _get_end_millis(self, idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        return p.get_end_millis() if isinstance(p, SimpleTimePeriod) else int(p.get_end().timestamp() * 1000)

    def _get_middle_millis(self, idx: int) -> int:
        p = self.get_data_item(idx).get_period()
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        return s + (e - s) // 2