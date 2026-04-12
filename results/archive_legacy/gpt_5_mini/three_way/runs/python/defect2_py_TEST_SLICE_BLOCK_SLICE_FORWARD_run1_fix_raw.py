def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(fraction * 255.0)
    g = max(0, min(g, 255))
    return (g, g, g)