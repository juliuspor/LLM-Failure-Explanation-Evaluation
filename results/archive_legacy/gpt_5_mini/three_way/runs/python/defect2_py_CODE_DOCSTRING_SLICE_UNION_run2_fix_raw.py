def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        g = 0
    else:
        g = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    g = int(round(g))
    g = max(0, min(255, g))
    return (g, g, g)