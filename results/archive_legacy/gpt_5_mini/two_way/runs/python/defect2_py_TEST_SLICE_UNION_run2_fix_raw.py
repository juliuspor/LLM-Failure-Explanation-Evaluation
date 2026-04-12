def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(min(value, self._upper_bound), self._lower_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)