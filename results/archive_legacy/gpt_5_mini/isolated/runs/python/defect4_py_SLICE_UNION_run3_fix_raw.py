def _update_bounds(self, period: TimePeriod, index: int) -> None:
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
    middle = start + ((end - start) // 2)
    def _get_start(i: int) -> int:
        p = self.get_data_item(i).get_period()
        if isinstance(p, SimpleTimePeriod):
            return p.get_start_millis()
        return int(p.get_start().timestamp() * 1000)
    def _get_end(i: int) -> int:
        p = self.get_data_item(i).get_period()
        if isinstance(p, SimpleTimePeriod):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)
    def _get_middle(i: int) -> int:
        s = _get_start(i)
        e = _get_end(i)
        return s + ((e - s) // 2)
    if self._min_start_index >= 0:
        try:
            min_start = _get_start(self._min_start_index)
        except Exception:
            min_start = None
        if min_start is None:
            self._min_start_index = index
        else:
            if start < min_start:
                self._min_start_index = index
    else:
        self._min_start_index = index
    if self._max_start_index >= 0:
        try:
            max_start = _get_start(self._max_start_index)
        except Exception:
            max_start = None
        if max_start is None:
            self._max_start_index = index
        else:
            if start > max_start:
                self._max_start_index = index
    else:
        self._max_start_index = index
    if self._min_middle_index >= 0:
        try:
            min_middle = _get_middle(self._min_middle_index)
        except Exception:
            min_middle = None
        if min_middle is None:
            self._min_middle_index = index
        else:
            if middle < min_middle:
                self._min_middle_index = index
    else:
        self._min_middle_index = index
    if self._max_middle_index >= 0:
        try:
            max_middle = _get_middle(self._max_middle_index)
        except Exception:
            max_middle = None
        if max_middle is None:
            self._max_middle_index = index
        else:
            if middle > max_middle:
                self._max_middle_index = index
    else:
        self._max_middle_index = index
    if self._min_end_index >= 0:
        try:
            min_end = _get_end(self._min_end_index)
        except Exception:
            min_end = None
        if min_end is None:
            self._min_end_index = index
        else:
            if end < min_end:
                self._min_end_index = index
    else:
        self._min_end_index = index
    if self._max_end_index >= 0:
        try:
            max_end = _get_end(self._max_end_index)
        except Exception:
            max_end = None
        if max_end is None:
            self._max_end_index = index
        else:
            if end > max_end:
                self._max_end_index = index
    else:
        self._max_end_index = index