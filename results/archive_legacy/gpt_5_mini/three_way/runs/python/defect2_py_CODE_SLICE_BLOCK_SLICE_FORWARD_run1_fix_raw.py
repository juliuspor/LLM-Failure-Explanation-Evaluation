def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        g = 128
    else:
        g = int((v - self._lower_bound) / span * 255.0)
    g = max(0, min(255, g))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}, bounds=[{self._lower_bound},{self._upper_bound}]")
    return (g, g, g)