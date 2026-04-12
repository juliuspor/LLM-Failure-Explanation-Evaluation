def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound})")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    frac = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    frac = max(0.0, min(1.0, frac))
    g = int(frac * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Gray channel out of range: g={g} computed from value={value} bounds=[{self._lower_bound},{self._upper_bound}]")
    return (g, g, g)