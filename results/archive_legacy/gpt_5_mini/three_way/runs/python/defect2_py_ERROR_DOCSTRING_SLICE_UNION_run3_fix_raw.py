def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    v = max(self._lower_bound, min(value, self._upper_bound))
    normalized = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(normalized * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: r={g} g={g} b={g}")
    return (g, g, g)