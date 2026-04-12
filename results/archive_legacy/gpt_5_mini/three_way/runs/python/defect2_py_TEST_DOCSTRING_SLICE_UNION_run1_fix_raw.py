def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(min(value, self._upper_bound), self._lower_bound)
    if self._upper_bound == self._lower_bound:
        return (0, 0, 0)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)