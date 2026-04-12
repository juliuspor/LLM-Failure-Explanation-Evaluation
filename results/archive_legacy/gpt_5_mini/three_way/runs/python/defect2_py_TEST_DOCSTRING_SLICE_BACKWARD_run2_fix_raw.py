def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError("lower_bound and upper_bound must differ")
    frac = (v - self._lower_bound) / denom
    g = int(frac * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)