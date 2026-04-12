    def _update_bounds(self, period: TimePeriod, index: int) -> None:
        """
        Update cached min/max indices for the current bounds.

        This updates the indices tracking the minimum/maximum start, middle, and
        end timestamps across the series.

        Args:
            period: Time period for the newly added item.
            index: Index of the item within the series.
        """
        # Helper to get start and end milliseconds from any TimePeriod
        def get_start_millis(p: TimePeriod) -> int:
            if isinstance(p, SimpleTimePeriod):
                return p.get_start_millis()
            else:
                return int(p.get_start().timestamp() * 1000)
        
        def get_end_millis(p: TimePeriod) -> int:
            if isinstance(p, SimpleTimePeriod):
                return p.get_end_millis()
            else:
                return int(p.get_end().timestamp() * 1000)
        
        start = get_start_millis(period)
        end = get_end_millis(period)
        middle = start + ((end - start) // 2)
        
        # Update min start index
        if self._min_start_index >= 0:
            min_start = get_start_millis(self.get_data_item(self._min_start_index).get_period())
            if start < min_start:
                self._min_start_index = index
        else:
            self._min_start_index = index
        
        # Update max start index
        if self._max_start_index >= 0:
            max_start = get_start_millis(self.get_data_item(self._max_start_index).get_period())
            if start > max_start:
                self._max_start_index = index
        else:
            self._max_start_index = index
        
        # Update min middle index
        if self._min_middle_index >= 0:
            min_middle_period = self.get_data_item(self._min_middle_index).get_period()
            s = get_start_millis(min_middle_period)
            e = get_end_millis(min_middle_period)
            min_middle = s + (e - s) // 2
            if middle < min_middle:
                self._min_middle_index = index
        else:
            self._min_middle_index = index
        
        # Update max middle index
        if self._max_middle_index >= 0:
            # Bug fix: previously used self._min_middle_index instead of self._max_middle_index
            max_middle_period = self.get_data_item(self._max_middle_index).get_period()
            s = get_start_millis(max_middle_period)
            e = get_end_millis(max_middle_period)
            max_middle = s + (e - s) // 2
            if middle > max_middle:
                self._max_middle_index = index
        else:
            self._max_middle_index = index
        
        # Update min end index
        if self._min_end_index >= 0:
            min_end = get_end_millis(self.get_data_item(self._min_end_index).get_period())
            if end < min_end:
                self._min_end_index = index
        else:
            self._min_end_index = index
        
        # Update max end index
        if self._max_end_index >= 0:
            max_end = get_end_millis(self.get_data_item(self._max_end_index).get_period())
            if end > max_end:
                self._max_end_index = index
        else:
            self._max_end_index = index