def _update_bounds(self, period: TimePeriod, index: int) -> None:
    if len(self._data) == 0:
        self._min_start_index = -1
        self._max_start_index = -1
        self._min_middle_index = -1
        self._max_middle_index = -1
        self._min_end_index = -1
        self._max_end_index = -1
        return
    def millis_start(p: TimePeriod) -> int:
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)
    def millis_end(p: TimePeriod) -> int:
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)
    min_start_idx = 0
    max_start_idx = 0
    min_middle_idx = 0
    max_middle_idx = 0
    min_end_idx = 0
    max_end_idx = 0
    s0 = millis_start(self.get_data_item(0).get_period())
    e0 = millis_end(self.get_data_item(0).get_period())
    m0 = s0 + ((e0 - s0) // 2)
    for i in range(1, len(self._data)):
        p = self.get_data_item(i).get_period()
        s = millis_start(p)
        e = millis_end(p)
        m = s + ((e - s) // 2)
        if s < millis_start(self.get_data_item(min_start_idx).get_period()):
            min_start_idx = i
        if s > millis_start(self.get_data_item(max_start_idx).get_period()):
            max_start_idx = i
        if m < (millis_start(self.get_data_item(min_middle_idx).get_period()) + ((millis_end(self.get_data_item(min_middle_idx).get_period()) - millis_start(self.get_data_item(min_middle_idx).get_period())) // 2)):
            min_middle_idx = i
        if m > (millis_start(self.get_data_item(max_middle_idx).get_period()) + ((millis_end(self.get_data_item(max_middle_idx).get_period()) - millis_start(self.get_data_item(max_middle_idx).get_period())) // 2)):
            max_middle_idx = i
        if e < millis_end(self.get_data_item(min_end_idx).get_period()):
            min_end_idx = i
        if e > millis_end(self.get_data_item(max_end_idx).get_period()):
            max_end_idx = i
    self._min_start_index = min_start_idx
    self._max_start_index = max_start_idx
    self._min_middle_index = min_middle_idx
    self._max_middle_index = max_middle_idx
    self._min_end_index = min_end_idx
    self._max_end_index = max_end_idx