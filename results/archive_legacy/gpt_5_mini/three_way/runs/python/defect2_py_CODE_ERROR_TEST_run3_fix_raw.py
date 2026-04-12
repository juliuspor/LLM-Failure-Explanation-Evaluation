def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0:
        raise ValueError("Invalid paint scale with equal lower and upper bounds.")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")
    return (g, g, g)