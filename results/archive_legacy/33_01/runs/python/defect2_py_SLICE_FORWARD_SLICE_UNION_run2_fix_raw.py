def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound <= self._lower_bound:
        raise ValueError(f"Invalid bounds: upper={self._upper_bound} must be > lower={self._lower_bound}")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray value {g} outside range 0..255 for value={value} (clamped to {v}) with bounds [{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)