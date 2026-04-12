def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError(f"upper_bound ({self._upper_bound}) must be greater than lower_bound ({self._lower_bound})")
    frac = (v - self._lower_bound) / denom
    if frac < 0.0:
        frac = 0.0
    elif frac > 1.0:
        frac = 1.0
    g = int(frac * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component g={g} outside 0..255 for value={value}")
    return (g, g, g)