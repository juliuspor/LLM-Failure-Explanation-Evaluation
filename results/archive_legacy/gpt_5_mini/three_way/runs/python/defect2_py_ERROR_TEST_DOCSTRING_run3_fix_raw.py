def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        proportion = 0.0
    else:
        proportion = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    proportion = max(0.0, min(1.0, proportion))
    g = int(proportion * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
    return (g, g, g)