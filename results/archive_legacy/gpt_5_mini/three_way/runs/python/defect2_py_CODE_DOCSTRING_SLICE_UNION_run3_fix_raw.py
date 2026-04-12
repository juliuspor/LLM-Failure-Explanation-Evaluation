def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        raise ValueError("upper_bound must be different from lower_bound")
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: computed g={g}")
    return (g, g, g)