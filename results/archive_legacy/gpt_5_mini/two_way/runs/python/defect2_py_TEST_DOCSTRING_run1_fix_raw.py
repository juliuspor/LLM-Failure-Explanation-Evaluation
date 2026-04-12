def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    elif v > self._upper_bound:
        v = self._upper_bound
    if self._upper_bound == self._lower_bound:
        frac = 0.0
    else:
        frac = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(frac * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)
