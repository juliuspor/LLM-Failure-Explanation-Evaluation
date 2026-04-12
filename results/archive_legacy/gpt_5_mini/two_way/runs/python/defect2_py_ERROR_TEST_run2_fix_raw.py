def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        g = 0
    else:
        normalized = (v - self._lower_bound) / range_span
        g = int(normalized * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)