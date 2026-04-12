def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    den = self._upper_bound - self._lower_bound
    if den == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound and upper_bound must differ (got {self._lower_bound})")
    fraction = (v - self._lower_bound) / den
    g = int(round(fraction * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)