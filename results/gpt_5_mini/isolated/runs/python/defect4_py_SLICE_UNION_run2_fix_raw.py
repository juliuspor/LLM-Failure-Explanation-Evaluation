def _update_bounds(self, period: TimePeriod, index: int) -> None:
    # Helper to get start/end in millis for any TimePeriod implementation
    def _get_start_millis(p: TimePeriod) -> int:
        if hasattr(p, 'get_start_millis') and callable(getattr(p, 'get_start_millis')):
            return p.get_start_millis()
        # fallback to datetime -> millis
        return int(p.get_start().timestamp() * 1000)

    def _get_end_millis(p: TimePeriod) -> int:
        if hasattr(p, 'get_end_millis') and callable(getattr(p, 'get_end_millis')):
            return p.get_end_millis()
        return int(p.get_end().timestamp() * 1000)

    start = _get_start_millis(period)
    end = _get_end_millis(period)
    middle = start + ((end - start) // 2)

    # min start
    if self._min_start_index >= 0:
        try:
            current = self.get_data_item(self._min_start_index).get_period()
            current_start = _get_start_millis(current)
            if start < current_start:
                self._min_start_index = index
        except Exception:
            # If retrieval fails, reset to new index
            self._min_start_index = index
    else:
        self._min_start_index = index

    # max start
    if self._max_start_index >= 0:
        try:
            current = self.get_data_item(self._max_start_index).get_period()
            current_start = _get_start_millis(current)
            if start > current_start:
                self._max_start_index = index
        except Exception:
            self._max_start_index = index
    else:
        self._max_start_index = index

    # min middle
    if self._min_middle_index >= 0:
        try:
            current = self.get_data_item(self._min_middle_index).get_period()
            cs = _get_start_millis(current)
            ce = _get_end_millis(current)
            current_middle = cs + ((ce - cs) // 2)
            if middle < current_middle:
                self._min_middle_index = index
        except Exception:
            self._min_middle_index = index
    else:
        self._min_middle_index = index

    # max middle
    if self._max_middle_index >= 0:
        try:
            current = self.get_data_item(self._max_middle_index).get_period()
            cs = _get_start_millis(current)
            ce = _get_end_millis(current)
            current_middle = cs + ((ce - cs) // 2)
            if middle > current_middle:
                self._max_middle_index = index
        except Exception:
            self._max_middle_index = index
    else:
        self._max_middle_index = index

    # min end
    if self._min_end_index >= 0:
        try:
            current = self.get_data_item(self._min_end_index).get_period()
            current_end = _get_end_millis(current)
            if end < current_end:
                self._min_end_index = index
        except Exception:
            self._min_end_index = index
    else:
        self._min_end_index = index

    # max end
    if self._max_end_index >= 0:
        try:
            current = self.get_data_item(self._max_end_index).get_period()
            current_end = _get_end_millis(current)
            if end > current_end:
                self._max_end_index = index
        except Exception:
            self._max_end_index = index
    else:
        self._max_end_index = index