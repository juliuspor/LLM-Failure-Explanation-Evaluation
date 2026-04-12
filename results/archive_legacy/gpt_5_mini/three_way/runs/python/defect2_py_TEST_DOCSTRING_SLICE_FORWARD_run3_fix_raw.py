def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    normalized = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if normalized < 0.0:
        normalized = 0.0
    elif normalized > 1.0:
        normalized = 1.0
    g = int(normalized * 255.0)
    return (g, g, g)