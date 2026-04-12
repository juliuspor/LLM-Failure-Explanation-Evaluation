def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        g = 0
    else:
        t = (v - self._lower_bound) / range_span
        t = max(0.0, min(1.0, t))
        g = int(t * 255.0)
    return (g, g, g)