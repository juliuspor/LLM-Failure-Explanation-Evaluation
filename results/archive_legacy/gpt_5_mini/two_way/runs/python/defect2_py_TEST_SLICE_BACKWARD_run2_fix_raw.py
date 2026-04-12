def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = min(max(value, self._lower_bound), self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        g = 0
    else:
        g = int((v - self._lower_bound) / denom * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)