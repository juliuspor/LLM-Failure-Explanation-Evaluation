def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)