def _update_bounds(self, period: TimePeriod, index: int) -> None:
    def get_start_end_millis(p: TimePeriod):
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis(), p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
            return s, e
    start, end = get_start_end_millis(period)
    middle = start + ((end - start) // 2)
    if self._min_start_index >= 0:
        s_min, _ = get_start_end_millis(self.get_data_item(self._min_start_index).get_period())
        if start < s_min:
            self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        s_max, _ = get_start_end_millis(self.get_data_item(self._max_start_index).get_period())
        if start > s_max:
            self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        s_minm, e_minm = get_start_end_millis(self.get_data_item(self._min_middle_index).get_period())
        min_middle = s_minm + ((e_minm - s_minm) // 2)
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        s_maxm, e_maxm = get_start_end_millis(self.get_data_item(self._max_middle_index).get_period())
        max_middle = s_maxm + ((e_maxm - s_maxm) // 2)
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        _, e_min = get_start_end_millis(self.get_data_item(self._min_end_index).get_period())
        if end < e_min:
            self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        _, e_max = get_start_end_millis(self.get_data_item(self._max_end_index).get_period())
        if end > e_max:
            self._max_end_index = index
    else:
        self._max_end_index = index