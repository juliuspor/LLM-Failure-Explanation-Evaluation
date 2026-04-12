def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError("Invalid bounds: lower_bound and upper_bound must differ")
    rel = (v - self._lower_bound) / denom
    g = int(round(rel * 255.0))
    g = max(0, min(255, g))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")
    return (g, g, g)