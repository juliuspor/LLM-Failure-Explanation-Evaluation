def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0:
        g = 127
    else:
        g = int((v - self._lower_bound) / range_span * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)