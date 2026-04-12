def _update_bounds(self, period: TimePeriod, index: int) -> None:
    def millis(p: TimePeriod):
        if isinstance(p, SimpleTimePeriod):
            s = p.get_start_millis()
            e = p.get_end_millis()
        else:
            s = int(p.get_start().timestamp() * 1000)
            e = int(p.get_end().timestamp() * 1000)
        return s, e, s + ((e - s) // 2)

    start, end, middle = millis(period)

    if self._min_start_index >= 0:
        ms, me, mm = millis(self.get_data_item(self._min_start_index).get_period())
        if start < ms:
            self._min_start_index = index
    else:
        self._min_start_index = index

    if self._max_start_index >= 0:
        ms, me, mm = millis(self.get_data_item(self._max_start_index).get_period())
        if start > ms:
            self._max_start_index = index
    else:
        self._max_start_index = index

    if self._min_middle_index >= 0:
        ms, me, mm = millis(self.get_data_item(self._min_middle_index).get_period())
        if middle < mm:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    if self._max_middle_index >= 0:
        ms, me, mm = millis(self.get_data_item(self._max_middle_index).get_period())
        if middle > mm:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    if self._min_end_index >= 0:
        ms, me, mm = millis(self.get_data_item(self._min_end_index).get_period())
        if end < me:
            self._min_end_index = index
    else:
        self._min_end_index = index

    if self._max_end_index >= 0:
        ms, me, mm = millis(self.get_data_item(self._max_end_index).get_period())
        if end > me:
            self._max_end_index = index
    else:
        self._max_end_index = index