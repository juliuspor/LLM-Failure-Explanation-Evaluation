def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = float(value)
    if v < self._lower_bound:
        v = self._lower_bound
    if v > self._upper_bound:
        v = self._upper_bound
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")
    return (g, g, g)