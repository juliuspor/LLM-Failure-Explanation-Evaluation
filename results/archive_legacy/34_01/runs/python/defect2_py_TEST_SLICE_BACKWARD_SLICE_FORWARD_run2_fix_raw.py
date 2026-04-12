def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g_float = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    if g_float < 0.0:
        g_float = 0.0
    elif g_float > 255.0:
        g_float = 255.0
    g = int(g_float)
    return (g, g, g)