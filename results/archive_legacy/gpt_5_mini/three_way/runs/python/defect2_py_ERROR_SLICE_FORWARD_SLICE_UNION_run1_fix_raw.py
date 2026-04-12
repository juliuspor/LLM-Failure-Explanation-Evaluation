def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"upper_bound must not equal lower_bound: {self._lower_bound}")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    return (g, g, g)