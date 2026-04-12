def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(self._lower_bound, min(value, self._upper_bound))
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError(f"Cannot compute paint with zero range: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component {g} outside 0..255 for value={value}, lower={self._lower_bound}, upper={self._upper_bound}")
    return (g, g, g)