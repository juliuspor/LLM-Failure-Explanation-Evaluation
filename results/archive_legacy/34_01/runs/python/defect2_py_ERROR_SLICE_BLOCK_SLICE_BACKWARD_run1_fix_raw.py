def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound <= self._lower_bound:
        raise ValueError(f"Invalid bounds: lower_bound={self._lower_bound} upper_bound={self._upper_bound}")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    frac = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(frac * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)