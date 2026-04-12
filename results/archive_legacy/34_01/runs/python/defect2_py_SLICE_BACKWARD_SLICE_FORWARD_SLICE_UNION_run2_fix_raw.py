def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) equals upper_bound ({self._upper_bound})")
    g = int(round((v - self._lower_bound) / denom * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: computed {g}")
    return (g, g, g)