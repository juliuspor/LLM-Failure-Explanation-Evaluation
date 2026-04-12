    def _update_bounds(self, period: TimePeriod, index: int) -> None:
        if isinstance(period, SimpleTimePeriod):
            start = period.get_start_millis()
            end = period.get_end_millis()
        else:
            start = int(period.get_start().timestamp() * 1000)
            end = int(period.get_end().timestamp() * 1000)
        middle = start + ((end - start) // 2)

        if self._min_start_index >= 0:
            min_start_period = self.get_data_item(self._min_start_index).get_period()
            if isinstance(min_start_period, SimpleTimePeriod):
                min_start = min_start_period.get_start_millis()
            else:
                min_start = int(min_start_period.get_start().timestamp() * 1000)
            if start < min_start:
                self._min_start_index = index
        else:
            self._min_start_index = index

        if self._max_start_index >= 0:
            max_start_period = self.get_data_item(self._max_start_index).get_period()
            if isinstance(max_start_period, SimpleTimePeriod):
                max_start = max_start_period.get_start_millis()
            else:
                max_start = int(max_start_period.get_start().timestamp() * 1000)
            if start > max_start:
                self._max_start_index = index
        else:
            self._max_start_index = index

        if self._min_middle_index >= 0:
            min_middle_period = self.get_data_item(self._min_middle_index).get_period()
            if isinstance(min_middle_period, SimpleTimePeriod):
                min_middle = min_middle_period.get_start_millis() + (min_middle_period.get_end_millis() - min_middle_period.get_start_millis()) // 2
            else:
                min_middle = int(min_middle_period.get_start().timestamp() * 1000) + (int(min_middle_period.get_end().timestamp() * 1000) - int(min_middle_period.get_start().timestamp() * 1000)) // 2
            if middle < min_middle:
                self._min_middle_index = index
        else:
            self._min_middle_index = index

        if self._max_middle_index >= 0:
            max_middle_period = self.get_data_item(self._max_middle_index).get_period()
            if isinstance(max_middle_period, SimpleTimePeriod):
                max_middle = max_middle_period.get_start_millis() + (max_middle_period.get_end_millis() - max_middle_period.get_start_millis()) // 2
            else:
                max_middle = int(max_middle_period.get_start().timestamp() * 1000) + (int(max_middle_period.get_end().timestamp() * 1000) - int(max_middle_period.get_start().timestamp() * 1000)) // 2
            if middle > max_middle:
                self._max_middle_index = index
        else:
            self._max_middle_index = index

        if self._min_end_index >= 0:
            min_end_period = self.get_data_item(self._min_end_index).get_period()
            if isinstance(min_end_period, SimpleTimePeriod):
                min_end = min_end_period.get_end_millis()
            else:
                min_end = int(min_end_period.get_end().timestamp() * 1000)
            if end < min_end:
                self._min_end_index = index
        else:
            self._min_end_index = index

        if self._max_end_index >= 0:
            max_end_period = self.get_data_item(self._max_end_index).get_period()
            if isinstance(max_end_period, SimpleTimePeriod):
                max_end = max_end_period.get_end_millis()
            else:
                max_end = int(max_end_period.get_end().timestamp() * 1000)
            if end > max_end:
                self._max_end_index = index
        else:
            self._max_end_index = index

        return

    def _recalculate_bounds(self) -> None:
        self._min_start_index = -1
        self._min_middle_index = -1
        self._min_end_index = -1
        self._max_start_index = -1
        self._max_middle_index = -1
        self._max_end_index = -1
        for i in range(len(self._data)):
            tpv = self._data[i]
            self._update_bounds(tpv.get_period(), i)

    def update(self, index: int, value: float) -> None:
        item = self.get_data_item(index)
        item.set_value(value)
        self.fire_series_changed()

    def delete(self, start: int, end: int) -> None:
        for i in range(end - start + 1):
            del self._data[start]
        self._recalculate_bounds()
        self.fire_series_changed()

    def get_min_start_index(self) -> int:
        return self._min_start_index

    def get_max_start_index(self) -> int:
        return self._max_start_index

    def get_min_middle_index(self) -> int:
        return self._min_middle_index

    def get_max_middle_index(self) -> int:
        return self._max_middle_index

    def get_min_end_index(self) -> int:
        return self._min_end_index

    def get_max_end_index(self) -> int:
        return self._max_end_index

    def __eq__(self, other) -> bool:
        if other is self:
            return True
        if not isinstance(other, TimePeriodValues):
            return False
        if not super().__eq__(other):
            return False
        if self._domain != other._domain:
            return False
        if self._range != other._range:
            return False
        if len(self._data) != len(other._data):
            return False
        for i in range(len(self._data)):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __hash__(self) -> int:
        result = hash(self._domain) if self._domain else 0
        result = 29 * result + (hash(self._range) if self._range else )
        result = 29 * result + self._min_start_index
        result = 29 * result + self._max_start_index
        return result

    def clone(self) -> 'TimePeriodValues':
        return self.create_copy(0, self.get_item_count() - 1)

    def create_copy(self, start: int, end: int) -> 'TimePeriodValues':
        copy_obj = TimePeriodValues(self._key, self._domain, self._range)
        if len(self._data) > 0:
            for index in range(start, end + 1):
                item = self._data[index]
                clone_item = item.clone()
                copy_obj.add(clone_item)
        return copy_obj

    def __str__(self) -> str:
        return f"TimePeriodValues{{domain={self._domain}, range={self._range}, data={self._data}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._domain}, range={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._domain}, range={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def __repr__(self) -> str:
        return f"TimePeriodValues{{domain={self._range}}}}"

    def