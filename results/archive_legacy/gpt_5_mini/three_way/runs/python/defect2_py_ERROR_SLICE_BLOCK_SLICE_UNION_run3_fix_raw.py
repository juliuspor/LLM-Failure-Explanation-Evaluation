def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_span = self._upper_bound - self._lower_bound
    if range_span <= 0.0:
        raise ValueError(f"Invalid bounds: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")
    g = int((v - self._lower_bound) / range_span * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}, value={value}, bounds=[{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)