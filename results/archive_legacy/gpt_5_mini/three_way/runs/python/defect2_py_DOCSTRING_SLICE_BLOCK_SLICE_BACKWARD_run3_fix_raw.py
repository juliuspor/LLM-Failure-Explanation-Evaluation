def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Gray={g} for value={value} with bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)