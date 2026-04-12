def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: upper_bound equals lower_bound ({self._upper_bound})")
    g = int(round((v - self._lower_bound) / denom * 255.0))
    if g < 0 or g > 255:
        g = max(0, min(255, g))
    return (g, g, g)