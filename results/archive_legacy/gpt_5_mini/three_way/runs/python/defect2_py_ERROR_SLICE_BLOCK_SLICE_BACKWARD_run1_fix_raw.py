def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_ = self._upper_bound - self._lower_bound
    if range_ <= 0.0:
        raise ValueError(f"Invalid bounds: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")
    f = (v - self._lower_bound) / range_ * 255.0
    g = int(round(f))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)