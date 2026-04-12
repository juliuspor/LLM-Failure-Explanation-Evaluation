def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower={self._lower_bound} upper={self._upper_bound}")
    g = int(round((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0))
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    return (g, g, g)