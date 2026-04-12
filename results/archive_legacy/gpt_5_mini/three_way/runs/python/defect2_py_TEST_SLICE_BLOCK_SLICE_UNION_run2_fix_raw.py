def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = min(max(value, self._lower_bound), self._upper_bound)
    range_ = self._upper_bound - self._lower_bound
    if range_ == 0:
        g = 0
    else:
        g = int((v - self._lower_bound) / range_ * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)