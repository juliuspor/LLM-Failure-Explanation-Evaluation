def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    range_ = self._upper_bound - self._lower_bound
    if range_ == 0.0:
        g = 0
    else:
        g = int(round((v - self._lower_bound) / range_ * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)