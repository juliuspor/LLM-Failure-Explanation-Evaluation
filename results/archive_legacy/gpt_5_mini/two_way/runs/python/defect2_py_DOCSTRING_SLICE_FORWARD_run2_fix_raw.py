def get_paint(self, value: float) -> Tuple[int, int, int]:
    if value is None:
        raise ValueError("value must not be None")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / denom
    fraction = max(0.0, min(1.0, fraction))
    g = int(round(fraction * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: r={g},g={g},b={g}")
    return (g, g, g)