def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    diff = self._upper_bound - self._lower_bound
    if diff == 0:
        raise ValueError("upper_bound equals lower_bound; cannot scale value")
    g = int((v - self._lower_bound) / diff * 255.0)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)