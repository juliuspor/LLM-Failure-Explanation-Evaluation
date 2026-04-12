def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Get start and end as milliseconds consistently
    if isinstance(period, SimpleTimePeriod):
        start = period.get_start_millis()
        end = period.get_end_millis()
    else:
        start_dt = period.get_start()
        end_dt = period.get_end()
        if start_dt is None or end_dt is None:
            raise ValueError("TimePeriod get_start()/get_end() must return datetime values.")
        start = int(start_dt.timestamp() * 1000)
        end = int(end_dt.timestamp() * 1000)

    middle = start + ((end - start) // 2)

    # min start
    if self._min_start_index >= 0:
        min_start_period = self.get_data_item(self._min_start_index).get_period()
        if isinstance(min_start_period, SimpleTimePeriod):
            min_start = min_start_period.get_start_millis()
        else:
            ms = min_start_period.get_start()
            if ms is None:
                raise ValueError("TimePeriod get_start() must return datetime")
            min_start = int(ms.timestamp() * 1000)
        if start < min_start:
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0:
        max_start_period = self.get_data_item(self._max_start_index).get_period()
        if isinstance(max_start_period, SimpleTimePeriod):
            max_start = max_start_period.get_start_millis()
        else:
            ms = max_start_period.get_start()
            if ms is None:
                raise ValueError("TimePeriod get_start() must return datetime")
            max_start = int(ms.timestamp() * 1000)
        if start > max_start:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0:
        min_middle_period = self.get_data_item(self._min_middle_index).get_period()
        if isinstance(min_middle_period, SimpleTimePeriod):
            s = min_middle_period.get_start_millis()
            e = min_middle_period.get_end_millis()
        else:
            s_dt = min_middle_period.get_start()
            e_dt = min_middle_period.get_end()
            if s_dt is None or e_dt is None:
                raise ValueError("TimePeriod get_start()/get_end() must return datetime values.")
            s = int(s_dt.timestamp() * 1000)
            e = int(e_dt.timestamp() * 1000)
        min_middle = s + (e - s) // 2
        if middle < min_middle:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0:
        max_middle_period = self.get_data_item(self._max_middle_index).get_period()
        if isinstance(max_middle_period, SimpleTimePeriod):
            s = max_middle_period.get_start_millis()
            e = max_middle_period.get_end_millis()
        else:
            s_dt = max_middle_period.get_start()
            e_dt = max_middle_period.get_end()
            if s_dt is None or e_dt is None:
                raise ValueError("TimePeriod get_start()/get_end() must return datetime values.")
            s = int(s_dt.timestamp() * 1000)
            e = int(e_dt.timestamp() * 1000)
        max_middle = s + (e - s) // 2
        if middle > max_middle:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0:
        min_end_period = self.get_data_item(self._min_end_index).get_period()
        if isinstance(min_end_period, SimpleTimePeriod):
            min_end = min_end_period.get_end_millis()
        else:
            ed = min_end_period.get_end()
            if ed is None:
                raise ValueError("TimePeriod get_end() must return datetime")
            min_end = int(ed.timestamp() * 1000)
        if end < min_end:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0:
        max_end_period = self.get_data_item(self._max_end_index).get_period()
        if isinstance(max_end_period, SimpleTimePeriod):
            max_end = max_end_period.get_end_millis()
        else:
            ed = max_end_period.get_end()
            if ed is None:
                raise ValueError("TimePeriod get_end() must return datetime")
            max_end = int(ed.timestamp() * 1000)
        if end > max_end:
            self._max_end_index = index
    else:
        self._max_end_index = index