def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v <= self._lower_bound:
        return (0, 0, 0)
    if v >= self._upper_bound:
        return (255, 255, 255)
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    gray = int(fraction * 255.0)
    if gray < 0:
        gray = 0
    elif gray > 255:
        gray = 255
    return (gray, gray, gray)