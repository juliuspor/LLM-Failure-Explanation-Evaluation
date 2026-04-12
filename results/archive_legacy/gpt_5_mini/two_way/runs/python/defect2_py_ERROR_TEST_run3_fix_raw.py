def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / denom
    g = int(fraction * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)
