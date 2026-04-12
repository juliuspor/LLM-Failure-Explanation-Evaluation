def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError(f"Bounds must not be equal: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color components out of range for value={value}: r={g}, g={g}, b={g}")
    return (g, g, g)