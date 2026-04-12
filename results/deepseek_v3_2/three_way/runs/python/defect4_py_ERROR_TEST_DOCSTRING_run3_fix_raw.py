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
        
        # Helper to get start millis from a period at given index
        def get_start_millis(idx):
            p = self.get_data_item(idx).get_period()
            if isinstance(p, SimpleTimePeriod):
                return p.get_start_millis()
            else:
                return int(p.get_start().timestamp() * 1000)
        
        # Helper to get end millis from a period at given index
        def get_end_millis(idx):
            p = self.get_data_item(idx).get_period()
            if isinstance(p, SimpleTimePeriod):
                return p.get_end_millis()
            else:
                return int(p.get_end().timestamp() * 1000)
        
        # Helper to get middle millis from a period at given index
        def get_middle_millis(idx):
            p = self.get_data_item(idx).get_period()
            if isinstance(p, SimpleTimePeriod):
                s = p.get_start_millis()
                e = p.get_end_millis()
            else:
                s = int(p.get_start().timestamp() * 1000)
                e = int(p.get_end().timestamp() * 1000)
            return s + (e - s) // 2
        
        # Update min start index
        if self._min_start_index >= 0:
            min_start = get_start_millis(self._min_start_index)
            if start < min_start:
                self._min_start_index = index
        else:
            self._min_start_index = index
        
        # Update max start index
        if self._max_start_index >= 0:
            max_start = get_start_millis(self._max_start_index)
            if start > max_start:
                self._max_start_index = index
        else:
            self._max_start_index = index
        
        # Update min middle index
        if self._min_middle_index >= 0:
            min_middle = get_middle_millis(self._min_middle_index)
            if middle < min_middle:
                self._min_middle_index = index
        else:
            self._min_middle_index = index
        
        # Update max middle index
        if self._max_middle_index >= 0:
            max_middle = get_middle_millis(self._max_middle_index)
            if middle > max_middle:
                self._max_middle_index = index
        else:
            self._max_middle_index = index
        
        # Update min end index
        if self._min_end_index >= 0:
            min_end = get_end_millis(self._min_end_index)
            if end < min_end:
                self._min_end_index = index
        else:
            self._min_end_index = index
        
        # Update max end index
        if self._max_end_index >= 0:
            max_end = get_end_millis(self._max_end_index)
            if end > max_end:
                self._max_end_index = index
        else:
            self._max_end_index = index