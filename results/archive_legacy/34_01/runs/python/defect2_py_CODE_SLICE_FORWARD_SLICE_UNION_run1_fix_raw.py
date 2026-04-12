def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        return (0, 0, 0)
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g_float = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    g = int(round(g_float))
    g = max(0, min(255, g))
    return (g, g, g)