def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    g = int(round(max(0.0, min(255.0, g))))
    return (g, g, g)
