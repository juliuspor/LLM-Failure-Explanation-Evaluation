def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: upper and lower are equal ({self._lower_bound})")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside expected range: g={g}, value={value}, lower={self._lower_bound}, upper={self._upper_bound}")
    return (g, g, g)