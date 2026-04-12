def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("upper_bound must be greater than lower_bound")
    g = int(round((v - self._lower_bound) / span * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray level {g} outside of expected range 0-255")
    return (g, g, g)