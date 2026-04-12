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
        
        # Update min/max start
        if self._min_start_index < 0 or start < self.get_data_item(self._min_start_index).get_period().get_start_millis() if isinstance(self.get_data_item(self._min_start_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_start_index).get_period().get_start().timestamp() * 1000):
            self._min_start_index = index
        if self._max_start_index < 0 or start > self.get_data_item(self._max_start_index).get_period().get_start_millis() if isinstance(self.get_data_item(self._max_start_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_start_index).get_period().get_start().timestamp() * 1000):
            self._max_start_index = index
        
        # Update min/max middle
        if self._min_middle_index < 0 or middle < (self.get_data_item(self._min_middle_index).get_period().get_start_millis() + (self.get_data_item(self._min_middle_index).get_period().get_end_millis() - self.get_data_item(self._min_middle_index).get_period().get_start_millis()) // 2 if isinstance(self.get_data_item(self._min_middle_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_middle_index).get_period().get_start().timestamp() * 1000 + (self.get_data_item(self._min_middle_index).get_period().get_end().timestamp() * 1000 - self.get_data_item(self._min_middle_index).get_period().get_start().timestamp() * 1000) // 2)):
            self._min_middle_index = index
        if self._max_middle_index < 0 or middle > (self.get_data_item(self._max_middle_index).get_period().get_start_millis() + (self.get_data_item(self._max_middle_index).get_period().get_end_millis() - self.get_data_item(self._max_middle_index).get_period().get_start_millis()) // 2 if isinstance(self.get_data_item(self._max_middle_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_middle_index).get_period().get_start().timestamp() * 1000 + (self.get_data_item(self._max_middle_index).get_period().get_end().timestamp() * 1000 - self.get_data_item(self._max_middle_index).get_period().get_start().timestamp() * 1000) // 2)):
            self._max_middle_index = index
        
        # Update min/max end
        if self._min_end_index < 0 or end < self.get_data_item(self._min_end_index).get_period().get_end_millis() if isinstance(self.get_data_item(self._min_end_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._min_end_index).get_period().get_end().timestamp() * 1000):
            self._min_end_index = index
        if self._max_end_index < 0 or end > self.get_data_item(self._max_end_index).get_period().get_end_millis() if isinstance(self.get_data_item(self._max_end_index).get_period(), SimpleTimePeriod) else int(self.get_data_item(self._max_end_index).get_period().get_end().timestamp() * 1000):
            self._max_end_index = index