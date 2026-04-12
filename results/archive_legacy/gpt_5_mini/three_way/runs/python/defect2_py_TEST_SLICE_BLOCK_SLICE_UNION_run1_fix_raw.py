def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        normalized = 0.0
    else:
        normalized = (value - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if normalized < 0.0:
        normalized = 0.0
    elif normalized > 1.0:
        normalized = 1.0
    g = int(normalized * 255.0)
    return (g, g, g)