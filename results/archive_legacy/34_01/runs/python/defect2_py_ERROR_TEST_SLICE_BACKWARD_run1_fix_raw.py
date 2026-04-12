def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError("upper and lower bounds must differ")
    v = max(self._lower_bound, min(self._upper_bound, value))
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)