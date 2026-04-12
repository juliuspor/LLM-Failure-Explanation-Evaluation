def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0:
        frac = 0.0
    else:
        frac = (v - self._lower_bound) / span
    g = int(round(frac * 255.0))
    if g < 0:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
    if g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
    return (g, g, g)