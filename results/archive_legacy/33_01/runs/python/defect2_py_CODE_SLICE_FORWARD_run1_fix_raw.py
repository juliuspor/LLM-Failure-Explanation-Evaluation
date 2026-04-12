def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("upper_bound equals lower_bound; cannot scale value")
    g_float = (v - self._lower_bound) / span * 255.0
    g = int(round(g_float))
    g = max(0, min(255, g))
    return (g, g, g)