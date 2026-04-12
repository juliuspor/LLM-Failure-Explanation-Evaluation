def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound <= self._lower_bound:
        raise ValueError(f"upper_bound must be greater than lower_bound (got {self._upper_bound} <= {self._lower_bound})")
    v = max(self._lower_bound, min(value, self._upper_bound))
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Gray channel out of range: {g} (expected 0..255)")
    return (g, g, g)