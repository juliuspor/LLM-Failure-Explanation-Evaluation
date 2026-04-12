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
        
        # Update min_start_index
        current_min_start = float('inf') if self._min_start_index < 0 else self.get_data_item(self._min_start_index).get_period().get_start_millis() if isinstance(self.get_data_item(self._min_start_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_start_index).get_period().get_start().timestamp() * 1000)
        if start < current_min_start:
            self._min_start_index = index
        elif self._min_start_index < 0:
            self._min_start_index = index
        
        # Update max_start_index
        current_max_start = float('-inf') if self._max_start_index < 0 else self.get_data_item(self._max_start_index).get_period().get_start_millis() if isinstance(self.get_data_item(self._max_start_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_start_index).get_period().get_start().timestamp() * 1000)
        if start > current_max_start:
            self._max_start_index = index
        elif self._max_start_index < 0:
            self._max_start_index = index
        
        # Update min_middle_index
        current_min_middle = float('inf') if self._min_middle_index < 0 else (self.get_data_item(self._min_middle_index).get_period().get_start_millis() + (self.get_data_item(self._min_middle_index).get_period().get_end_millis() - self.get_data_item(self._min_middle_index).get_period().get_start_millis()) // 2) if isinstance(self.get_data_item(self._min_middle_index).get_period(), SimpleTimePeriod) else (int(self.get_data_item(self._min_middle_index).get_period().get_start().timestamp() * 1000) + (int(self.get_data_item(self._min_middle_index).get_period().get_end().timestamp() * 1000) - int(self.get_data_item(self._min_middle_index).get_period().get_start().timestamp() * 1000)) // 2)
        if middle < current_min_middle:
            self._min_middle_index = index
        elif self._min_middle_index < 0:
            self._min_middle_index = index
        
        # Update max_middle_index (fixed copy-paste error)
        current_max_middle = float('-inf') if self._max_middle_index < 0 else (self.get_data_item(self._max_middle_index).get_period().get_start_millis() + (self.get_data_item(self._max_middle_index).get_period().get_end_millis() - self.get_data_item(self._max_middle_index).get_period().get_start_millis()) // 2) if isinstance(self.get_data_item(self._max_middle_index).get_period(), SimpleTimePeriod) else (int(self.get_data_item(self._max_middle_index).get_period().get_start().timestamp() * 1000) + (int(self.get_data_item(self._max_middle_index).get_period().get_end().timestamp() * 1000) - int(self.get_data_item(self._max_middle_index).get_period().get_start().timestamp() * 1000)) // 2)
        if middle > current_max_middle:
            self._max_middle_index = index
        elif self._max_middle_index < 0:
            self._max_middle_index = index
        
        # Update min_end_index
        current_min_end = float('inf') if self._min_end_index < 0 else self.get_data_item(self._min_end_index).get_period().get_end_millis() if isinstance(self.get_data_item(self._min_end_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_end_index).get_period().get_end().timestamp() * 1000)
        if end < current_min_end:
            self._min_end_index = index
        elif self._min_end_index < 0:
            self._min_end_index = index
        
        # Update max_end_index
        current_max_end = float('-inf') if self._max_end_index < 0 else self.get_data_item(self._max_end_index).get_period().get_end_millis() if isinstance(self.get_data_item(self._max_end_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_end_index).get_period().get_end().timestamp() * 1000)
        if end > current_max_end:
            self._max_end_index = index
        elif self._max_end_index < 0:
            self._max_end_index = index