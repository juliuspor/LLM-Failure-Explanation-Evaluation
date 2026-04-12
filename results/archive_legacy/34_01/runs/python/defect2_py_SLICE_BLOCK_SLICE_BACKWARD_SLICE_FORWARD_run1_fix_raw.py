def get_paint(self, value: float) -> Tuple[int, int, int]:
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        fraction = 0.0
    else:
        fraction = (value - self._lower_bound) / denom
    if fraction < 0.0:
        fraction = 0.0
    elif fraction > 1.0:
        fraction = 1.0
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)