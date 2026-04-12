def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(self._upper_bound, value))
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"upper_bound must be greater than lower_bound: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"computed gray component out of range: g={g} (value={value}, lower_bound={self._lower_bound}, upper_bound={self._upper_bound})")
    return (g, g, g)