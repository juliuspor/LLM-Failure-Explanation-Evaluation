def get_paint(self, value: float) -> Tuple[int, int, int]:
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound == upper_bound == {self._lower_bound}")
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    elif v > self._upper_bound:
        v = self._upper_bound
    fraction = (v - self._lower_bound) / denom
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)