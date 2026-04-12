def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    elif v > self._upper_bound:
        v = self._upper_bound
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) must be < upper_bound ({self._upper_bound})")
    g = int((v - self._lower_bound) / span * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)