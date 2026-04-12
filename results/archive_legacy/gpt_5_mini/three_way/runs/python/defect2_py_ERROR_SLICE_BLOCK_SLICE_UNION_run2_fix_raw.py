def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    range_ = self._upper_bound - self._lower_bound
    if range_ == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound and upper_bound must differ ({self._lower_bound}, {self._upper_bound})")
    ratio = (v - self._lower_bound) / range_
    g = int(ratio * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)