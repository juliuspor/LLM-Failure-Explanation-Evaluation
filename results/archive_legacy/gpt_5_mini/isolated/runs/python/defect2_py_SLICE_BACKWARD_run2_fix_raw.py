def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    elif v > self._upper_bound:
        v = self._upper_bound
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        norm = 0.0
    else:
        norm = (v - self._lower_bound) / denom
    g = int(round(norm * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)