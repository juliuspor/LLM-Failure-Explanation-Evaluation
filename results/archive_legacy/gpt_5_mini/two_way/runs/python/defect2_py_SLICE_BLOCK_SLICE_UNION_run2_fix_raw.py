def get_paint(self, value: float) -> Tuple[int, int, int]:
    if value is None:
        raise ValueError(f"value must be a number, got: {value}")
    clamped = max(self._lower_bound, min(value, self._upper_bound))
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) and upper_bound ({self._upper_bound}) must differ")
    g = int((clamped - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray value out of range: {g} (expected 0..255)")
    return (g, g, g)