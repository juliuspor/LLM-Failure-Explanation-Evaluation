def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        normalized = 0.0
    else:
        normalized = (v - self._lower_bound) / span
    g = int(round(normalized * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Computed grayscale {g} outside 0-255 for input value {value} (clamped to {v})")
    return (g, g, g)