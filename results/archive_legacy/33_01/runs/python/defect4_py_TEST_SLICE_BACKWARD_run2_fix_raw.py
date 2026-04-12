def _update_bounds(self, period: TimePeriod, index: int) -> None:
    min_start = None
    max_start = None
    min_middle = None
    max_middle = None
    min_end = None
    max_end = None
    self._min_start_index = -1
    self._max_start_index = -1
    self._min_middle_index = -1
    self._max_middle_index = -1
    self._min_end_index = -1
    self._max_end_index = -1
    for i, tpv in enumerate(self._data):
        p = tpv.get_period()
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        m = s + ((e - s) // 2)
        if min_start is None or s < min_start:
            min_start = s
            self._min_start_index = i
        if max_start is None or s > max_start:
            max_start = s
            self._max_start_index = i
        if min_middle is None or m < min_middle:
            min_middle = m
            self._min_middle_index = i
        if max_middle is None or m > max_middle:
            max_middle = m
            self._max_middle_index = i
        if min_end is None or e < min_end:
            min_end = e
            self._min_end_index = i
        if max_end is None or e > max_end:
            max_end = e
            self._max_end_index = i
    return None