def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    if v > self._upper_bound:
        v = self._upper_bound
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    return (g, g, g)