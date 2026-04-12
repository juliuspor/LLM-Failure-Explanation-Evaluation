    def _update_bounds(self, period: TimePeriod, index: int) -> None:
        """
        Update cached min/max indices for the current bounds.

        This updates the indices tracking the minimum/maximum start, middle, and
        end timestamps across the series.

        Args:
            period: Time period for the newly added item.
            index: Index of the item within the series.
        """
        # Get start and end as milliseconds
        if isinstance(period, SimpleTimePeriod):
            start = period.get_start_millis()
            end = period.get_end_millis()
        else:
            start = int(period.get_start().timestamp() * 1000)
            end = int(period.get_end().timestamp() * 1000)
        
        middle = start + ((end - start) // 2)
        
        # Helper to get milliseconds from a period at given index
        def get_start_millis_at(idx):
            p = self.get_data_item(idx).get_period()
            if isinstance(p, SimpleTimePeriod):
                return p.get_start_millis()
            else:
                return int(p.get_start().timestamp() * 1000)
        
        def get_end_millis_at(idx):
            p = self.get_data_item(idx).get_period()
            if isinstance(p, SimpleTimePeriod):
                return p.get_end_millis()
            else:
                return int(p.get_end().timestamp() * 1000)
        
        def get_middle_millis_at(idx):
            p = self.get_data_item(idx).get_period()
            if isinstance(p, SimpleTimePeriod):
                s = p.get_start_millis()
                e = p.get_end_millis()
            else:
                s = int(p.get_start().timestamp() * 1000)
                e = int(p.get_end().timestamp() * 1000)
            return s + (e - s) // 2
        
        # Update min start index
        if self._min_start_index == -1:
            self._min_start_index = index
        else:
            cur_min_start = get_start_millis_at(self._min_start_index)
            if start < cur_min_start:
                self._min_start_index = index
            elif start == cur_min_start and index < self._min_start_index:
                # Tie‑break: keep the smaller index
                self._min_start_index = index
        
        # Update max start index
        if self._max_start_index == -1:
            self._max_start_index = index
        else:
            cur_max_start = get_start_millis_at(self._max_start_index)
            if start > cur_max_start:
                self._max_start_index = index
            elif start == cur_max_start and index > self._max_start_index:
                # Tie‑break: keep the larger index (or could keep first, but max start should be later index if equal)
                self._max_start_index = index
        
        # Update min middle index
        if self._min_middle_index == -1:
            self._min_middle_index = index
        else:
            cur_min_middle = get_middle_millis_at(self._min_middle_index)
            if middle < cur_min_middle:
                self._min_middle_index = index
            elif middle == cur_min_middle and index < self._min_middle_index:
                self._min_middle_index = index
        
        # Update max middle index
        if self._max_middle_index == -1:
            self._max_middle_index = index
        else:
            # BUG FIX: previously used self._min_middle_index instead of self._max_middle_index
            cur_max_middle = get_middle_millis_at(self._max_middle_index)
            if middle > cur_max_middle:
                self._max_middle_index = index
            elif middle == cur_max_middle and index > self._max_middle_index:
                self._max_middle_index = index
        
        # Update min end index
        if self._min_end_index == -1:
            self._min_end_index = index
        else:
            cur_min_end = get_end_millis_at(self._min_end_index)
            if end < cur_min_end:
                self._min_end_index = index
            elif end == cur_min_end and index < self._min_end_index:
                self._min_end_index = index
        
        # Update max end index
        if self._max_end_index == -1:
            self._max_end_index = index
        else:
            cur_max_end = get_end_millis_at(self._max_end_index)
            if end > cur_max_end:
                self._max_end_index = index
            elif end == cur_max_end and index > self._max_end_index:
                self._max_end_index = index