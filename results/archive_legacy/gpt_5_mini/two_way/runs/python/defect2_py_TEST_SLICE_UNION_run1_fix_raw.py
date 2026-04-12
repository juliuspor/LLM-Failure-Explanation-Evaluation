def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError("upper_bound must not equal lower_bound")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    norm = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if norm < 0.0:
        norm = 0.0
    elif norm > 1.0:
        norm = 1.0
    g = int(norm * 255.0)
    return (g, g, g)