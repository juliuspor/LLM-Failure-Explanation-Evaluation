def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower==upper=={self._lower_bound}")
    if v < self._lower_bound:
        v = self._lower_bound
    elif v > self._upper_bound:
        v = self._upper_bound
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if ratio < 0.0:
        ratio = 0.0
    elif ratio > 1.0:
        ratio = 1.0
    g = int(round(ratio * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)