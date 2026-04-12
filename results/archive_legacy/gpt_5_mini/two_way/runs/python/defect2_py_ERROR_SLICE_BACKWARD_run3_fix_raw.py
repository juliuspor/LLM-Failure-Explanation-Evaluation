def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(min(value, self._upper_bound), self._lower_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound {self._lower_bound} equals upper_bound {self._upper_bound}")
    fraction = (v - self._lower_bound) / span
    g = int(fraction * 255.0)
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    return (g, g, g)