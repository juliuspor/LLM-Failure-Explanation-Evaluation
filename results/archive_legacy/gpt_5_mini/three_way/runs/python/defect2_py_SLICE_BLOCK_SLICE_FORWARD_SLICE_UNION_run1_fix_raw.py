def get_paint(self, value: float) -> Tuple[int, int, int]:
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError(f"Invalid bounds: upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound})")
    v = max(self._lower_bound, min(self._upper_bound, value))
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed color channel out of range: g={g} for value={value} with bounds [{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)