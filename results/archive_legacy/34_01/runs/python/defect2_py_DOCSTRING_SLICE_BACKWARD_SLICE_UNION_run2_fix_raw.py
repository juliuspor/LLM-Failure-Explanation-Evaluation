def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        g = 128
    else:
        normalized = (v - self._lower_bound) / denom
        g = int(round(normalized * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)