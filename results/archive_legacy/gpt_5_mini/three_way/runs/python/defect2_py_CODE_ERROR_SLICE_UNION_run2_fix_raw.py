def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = min(max(value, self._lower_bound), self._upper_bound)
    diff = self._upper_bound - self._lower_bound
    if diff == 0.0:
        raise ValueError("upper_bound must be different from lower_bound")
    g = int((v - self._lower_bound) / diff * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")
    return (g, g, g)