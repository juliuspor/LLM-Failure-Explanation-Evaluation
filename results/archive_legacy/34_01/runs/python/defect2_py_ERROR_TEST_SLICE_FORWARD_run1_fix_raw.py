def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    norm = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(norm * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)