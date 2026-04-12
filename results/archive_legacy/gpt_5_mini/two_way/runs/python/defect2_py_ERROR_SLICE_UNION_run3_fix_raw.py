def get_paint(self, value: float) -> Tuple[int, int, int]:
    if not (self._lower_bound <= value <= self._upper_bound):
        raise ValueError(f"value {value} outside bounds [{self._lower_bound}, {self._upper_bound}]")
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError(f"upper_bound ({self._upper_bound}) must be greater than lower_bound ({self._lower_bound})")
    normalized = (value - self._lower_bound) / span
    g = int(round(normalized * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"computed gray {g} outside 0..255 for value {value} and bounds [{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)