def _update_bounds(self, period: TimePeriod, index: int) -> None:
    self._min_start_index = -1
    self._max_start_index = -1
    self._min_middle_index = -1
    self._max_middle_index = -1
    self._min_end_index = -1
    self._max_end_index = -1
    if not self._data:
        return
    for i, tpv in enumerate(self._data):
        p = tpv.get_period()
        if isinstance(p, SimpleTimePeriod):
            start = p.get_start_millis()
            end = p.get_end_millis()
        else:
            start = int(p.get_start().timestamp() * 1000)
            end = int(p.get_end().timestamp() * 1000)
        middle = start + ((end - start) // 2)
        if self._min_start_index == -1 or start < (self.get_data_item(self._min_start_index).get_period().get_start_millis() if isinstance(self.get_data_item(self._min_start_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_start_index).get_period().get_start().timestamp() * 1000)):
            self._min_start_index = i
        if self._max_start_index == -1 or start > (self.get_data_item(self._max_start_index).get_period().get_start_millis() if isinstance(self.get_data_item(self._max_start_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_start_index).get_period().get_start().timestamp() * 1000)):
            self._max_start_index = i
        if self._min_middle_index == -1 or middle < (lambda idx: (lambda pp: (pp.get_start_millis() if isinstance(pp, SimpleTimePeriod) else int(pp.get_start().timestamp() * 1000)) + ((pp.get_end_millis() if isinstance(pp, SimpleTimePeriod) else int(pp.get_end().timestamp() * 1000)) - (pp.get_start_millis() if isinstance(pp, SimpleTimePeriod) else int(pp.get_start().timestamp() * 1000))) // 2))(self.get_data_item(idx).get_period())
                                             )(self._min_middle_index):
            self._min_middle_index = i
        if self._max_middle_index == -1 or middle > (lambda idx: (lambda pp: (pp.get_start_millis() if isinstance(pp, SimpleTimePeriod) else int(pp.get_start().timestamp() * 1000)) + ((pp.get_end_millis() if isinstance(pp, SimpleTimePeriod) else int(pp.get_end().timestamp() * 1000)) - (pp.get_start_millis() if isinstance(pp, SimpleTimePeriod) else int(pp.get_start().timestamp() * 1000))) // 2))(self.get_data_item(idx).get_period())
                                             )(self._max_middle_index):
            self._max_middle_index = i
        if self._min_end_index == -1 or end < (self.get_data_item(self._min_end_index).get_period().get_end_millis() if isinstance(self.get_data_item(self._min_end_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_end_index).get_period().get_end().timestamp() * 1000)):
            self._min_end_index = i
        if self._max_end_index == -1 or end > (self.get_data_item(self._max_end_index).get_period().get_end_millis() if isinstance(self.get_data_item(self._max_end_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_end_index).get_period().get_end().timestamp() * 1000)):
            self._max_end_index = i
    return None