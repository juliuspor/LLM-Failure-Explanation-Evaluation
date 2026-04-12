def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound <= self._lower_bound:
        raise ValueError(f"Invalid bounds: upper_bound must be greater than lower_bound (got {self._lower_bound}, {self._upper_bound})")
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"value {value} outside bounds [{self._lower_bound}, {self._upper_bound}]")
    fraction = (value - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(fraction * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray channel {g} out of range 0-255 for value {value} with bounds [{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)