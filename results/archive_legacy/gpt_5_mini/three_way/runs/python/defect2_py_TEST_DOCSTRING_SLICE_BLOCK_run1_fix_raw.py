def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    gray = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if gray < 0:
        gray = 0
    elif gray > 255:
        gray = 255
    return (gray, gray, gray)