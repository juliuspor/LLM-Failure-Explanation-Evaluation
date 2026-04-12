def get_paint(self, value: float) -> Tuple[int, int, int]:
    if value is None or not isinstance(value, (int, float)):
        raise TypeError("value must be a numeric type")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    fraction = 0.0 if span == 0 else (v - self._lower_bound) / span
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)