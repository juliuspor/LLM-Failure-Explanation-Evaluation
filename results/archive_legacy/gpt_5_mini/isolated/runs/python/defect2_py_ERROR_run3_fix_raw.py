def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("Invalid paint scale with zero span")
    fraction = (v - self._lower_bound) / span
    g = int(round(fraction * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color component out of range: {g}")
    return (g, g, g)