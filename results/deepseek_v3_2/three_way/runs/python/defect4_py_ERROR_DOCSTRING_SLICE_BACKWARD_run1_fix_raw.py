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
        
        # Helper to get milliseconds from a cached period
        def get_start_ms(p):
            if isinstance(p, SimpleTimePeriod):
                return p.get_start_millis()
            else:
                return int(p.get_start().timestamp() * 1000)
        
        def get_end_ms(p):
            if isinstance(p, SimpleTimePeriod):
                return p.get_end_millis()
            else:
                return int(p.get_end().timestamp() * 1000)
        
        def get_middle_ms(p):
            s = get_start_ms(p)
            e = get_end_ms(p)
            return s + ((e - s) // 2)
        
        # Update min_start
        if self._min_start_index >= 0:
            cached_period = self.get_data_item(self._min_start_index).get_period()
            cached_start = get_start_ms(cached_period)
            if start < cached_start:
                self._min_start_index = index
        else:
            self._min_start_index = index
        
        # Update max_start
        if self._max_start_index >= 0:
            cached_period = self.get_data_item(self._max_start_index).get_period()
            cached_start = get_start_ms(cached_period)
            if start > cached_start:
                self._max_start_index = index
        else:
            self._max_start_index = index
        
        # Update min_middle
        if self._min_middle_index >= 0:
            cached_period = self.get_data_item(self._min_middle_index).get_period()
            cached_middle = get_middle_ms(cached_period)
            if middle < cached_middle:
                self._min_middle_index = index
        else:
            self._min_middle_index = index
        
        # Update max_middle
        if self._max_middle_index >= 0:
            cached_period = self.get_data_item(self._max_middle_index).get_period()
            cached_middle = get_middle_ms(cached_period)
            if middle > cached_middle:
                self._max_middle_index = index
        else:
            self._max_middle_index = index
        
        # Update min_end
        if self._min_end_index >= 0:
            cached_period = self.get_data_item(self._min_end_index).get_period()
            cached_end = get_end_ms(cached_period)
            if end < cached_end:
                self._min_end_index = index
        else:
            self._min_end_index = index
        
        # Update max_end
        if self._max_end_index >= 0:
            cached_period = self.get_data_item(self._max_end_index).get_period()
            cached_end = get_end_ms(cached_period)
            if end > cached_end:
                self._max_end_index = index
        else:
            self._max_end_index = index