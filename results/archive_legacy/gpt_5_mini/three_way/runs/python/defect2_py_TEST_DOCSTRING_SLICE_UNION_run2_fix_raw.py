def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        return (0, 0, 0)
    v = min(max(value, self._lower_bound), self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)