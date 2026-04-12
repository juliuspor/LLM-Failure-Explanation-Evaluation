def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_ = self._upper_bound - self._lower_bound
    if range_ == 0:
        g = 0
    else:
        frac = (v - self._lower_bound) / range_
        g = int(round(frac * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)