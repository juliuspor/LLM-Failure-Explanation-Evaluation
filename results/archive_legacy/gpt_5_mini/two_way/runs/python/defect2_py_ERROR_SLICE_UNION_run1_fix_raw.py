def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) and upper_bound ({self._upper_bound}) must differ")
    g = int((v - self._lower_bound) / span * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Gray channel out of range: {g} (expected 0..255)")
    return (g, g, g)