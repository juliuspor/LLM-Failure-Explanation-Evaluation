def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    if v > self._upper_bound:
        v = self._upper_bound
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        normalized = 0.0
    else:
        normalized = (v - self._lower_bound) / span
    g = int(normalized * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)