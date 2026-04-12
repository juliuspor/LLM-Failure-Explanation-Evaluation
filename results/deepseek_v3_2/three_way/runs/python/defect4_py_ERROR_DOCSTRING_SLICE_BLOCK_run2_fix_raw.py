    def _update_bounds(self, period: TimePeriod, index: int) -> None:
        start = int(period.get_start().timestamp() * 1000)
        end = int(period.get_end().timestamp() * 1000)
        middle = start + ((end - start) // 2)
        
        if self._min_start_index >= 0:
            min_start_period = self.get_data_item(self._min_start_index).get_period()
            min_start = int(min_start_period.get_start().timestamp() * 1000)
            if start < min_start:
                self._min_start_index = index
        else:
            self._min_start_index = index
        
        if self._max_start_index >= 0:
            max_start_period = self.get_data_item(self._max_start_index).get_period()
            max_start = int(max_start_period.get_start().timestamp() * 1000)
            if start > max_start:
                self._max_start_index = index
        else:
            self._max_start_index = index
        
        if self._min_middle_index >= 0:
            min_middle_period = self.get_data_item(self._min_middle_index).get_period()
            s = int(min_middle_period.get_start().timestamp() * 1000)
            e = int(min_middle_period.get_end().timestamp() * 1000)
            min_middle = s + (e - s) // 2
            if middle < min_middle:
                self._min_middle_index = index
        else:
            self._min_middle_index = index
        
        if self._max_middle_index >= 0:
            max_middle_period = self.get_data_item(self._max_middle_index).get_period()
            s = int(max_middle_period.get_start().timestamp() * 1000)
            e = int(max_middle_period.get_end().timestamp() * 1000)
            max_middle = s + (e - s) // 2
            if middle > max_middle:
                self._max_middle_index = index
        else:
            self._max_middle_index = index
        
        if self._min_end_index >= 0:
            min_end_period = self.get_data_item(self._min_end_index).get_period()
            min_end = int(min_end_period.get_end().timestamp() * 1000)
            if end < min_end:
                self._min_end_index = index
        else:
            self._min_end_index = index
        
        if self._max_end_index >= 0:
            max_end_period = self.get_data_item(self._max_end_index).get_period()
            max_end = int(max_end_period.get_end().timestamp() * 1000)
            if end > max_end:
                self._max_end_index = index
        else:
            self._max_end_index = index