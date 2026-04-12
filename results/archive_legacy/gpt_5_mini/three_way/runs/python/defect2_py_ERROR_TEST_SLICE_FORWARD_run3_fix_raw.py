def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    if self._upper_bound == self._lower_bound:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    fraction = max(0.0, min(1.0, fraction))
    g = int(round(fraction * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)