def get_paint(self, value: float) -> Tuple[int, int, int]:
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"value {value} outside bounds [{self._lower_bound}, {self._upper_bound}]")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("upper_bound and lower_bound must not be equal")
    g = int(round((v - self._lower_bound) / span * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)