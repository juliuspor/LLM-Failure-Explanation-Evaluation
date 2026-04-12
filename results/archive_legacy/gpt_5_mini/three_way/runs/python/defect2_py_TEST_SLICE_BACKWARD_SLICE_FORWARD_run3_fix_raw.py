def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError("upper_bound must be different from lower_bound")
    v = min(max(value, self._lower_bound), self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)
    return (g, g, g)