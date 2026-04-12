def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / span
    g = int(round(fraction * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)