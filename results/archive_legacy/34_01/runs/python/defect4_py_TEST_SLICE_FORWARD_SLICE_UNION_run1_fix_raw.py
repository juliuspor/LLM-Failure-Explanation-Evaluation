def _update_bounds(self, period: TimePeriod, index: int) -> None:
    min_start_idx = -1
    max_start_idx = -1
    min_middle_idx = -1
    max_middle_idx = -1
    min_end_idx = -1
    max_end_idx = -1
    min_start_val = None
    max_start_val = None
    min_middle_val = None
    max_middle_val = None
    min_end_val = None
    max_end_val = None
    for i, tpv in enumerate(self._data):
        p = tpv.get_period()
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        m = s + ((e - s) // 2)
        if min_start_idx == -1 or s < min_start_val:
            min_start_idx = i
            min_start_val = s
        if max_start_idx == -1 or s > max_start_val:
            max_start_idx = i
            max_start_val = s
        if min_middle_idx == -1 or m < min_middle_val:
            min_middle_idx = i
            min_middle_val = m
        if max_middle_idx == -1 or m > max_middle_val:
            max_middle_idx = i
            max_middle_val = m
        if min_end_idx == -1 or e < min_end_val:
            min_end_idx = i
            min_end_val = e
        if max_end_idx == -1 or e > max_end_val:
            max_end_idx = i
            max_end_val = e
    self._min_start_index = min_start_idx
    self._max_start_index = max_start_idx
    self._min_middle_index = min_middle_idx
    self._max_middle_index = max_middle_idx
    self._min_end_index = min_end_idx
    self._max_end_index = max_end_idx
    return None