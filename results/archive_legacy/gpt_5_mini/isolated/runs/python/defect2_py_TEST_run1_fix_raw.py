def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    fraction = max(0.0, min(1.0, fraction))
    g = int(fraction * 255)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
    return (g, g, g)