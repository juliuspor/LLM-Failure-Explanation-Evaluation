def get_paint(self, value: float) -> Tuple[int, int, int]:
    if not isinstance(value, (int, float)):
        raise TypeError(f"value must be numeric, got {type(value)!r}")
    if value != value:
        raise ValueError("value is NaN")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    return (g, g, g)