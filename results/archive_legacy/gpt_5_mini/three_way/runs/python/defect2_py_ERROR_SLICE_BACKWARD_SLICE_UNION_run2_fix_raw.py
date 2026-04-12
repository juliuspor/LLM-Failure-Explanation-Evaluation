def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError(f"upper_bound ({self._upper_bound}) must be > lower_bound ({self._lower_bound})")
    g = int((v - self._lower_bound) / span * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)