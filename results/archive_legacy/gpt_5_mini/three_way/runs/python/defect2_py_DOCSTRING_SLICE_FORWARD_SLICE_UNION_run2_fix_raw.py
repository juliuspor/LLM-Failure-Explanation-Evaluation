def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound}); cannot map value")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed channel out of 0-255 range: g={g} for value={value} with bounds [{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)