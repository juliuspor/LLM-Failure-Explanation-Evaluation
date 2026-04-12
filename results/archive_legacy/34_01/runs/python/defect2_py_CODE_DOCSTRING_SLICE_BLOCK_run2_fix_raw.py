def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        return (0, 0, 0)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
    return (g, g, g)