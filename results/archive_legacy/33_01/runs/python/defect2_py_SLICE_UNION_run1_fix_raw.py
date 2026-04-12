def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound})")
    range_ = self._upper_bound - self._lower_bound
    ratio = (value - self._lower_bound) / range_
    if ratio < 0.0 or ratio > 1.0:
        raise ValueError(f"value {value} out of range [{self._lower_bound}, {self._upper_bound}] (ratio={ratio})")
    g = int(ratio * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)