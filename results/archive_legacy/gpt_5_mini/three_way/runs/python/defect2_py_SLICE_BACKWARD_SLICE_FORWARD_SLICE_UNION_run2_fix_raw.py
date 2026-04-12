def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    lower = self._lower_bound
    upper = self._upper_bound
    if upper == lower:
        g = 128
    else:
        ratio = (v - lower) / (upper - lower)
        g = int(round(ratio * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)