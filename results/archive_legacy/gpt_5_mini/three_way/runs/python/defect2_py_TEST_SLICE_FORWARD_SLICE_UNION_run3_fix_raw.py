def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        raise ValueError("upper_bound must be different from lower_bound")
    frac = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if frac < 0.0:
        frac = 0.0
    elif frac > 1.0:
        frac = 1.0
    g = int(frac * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)