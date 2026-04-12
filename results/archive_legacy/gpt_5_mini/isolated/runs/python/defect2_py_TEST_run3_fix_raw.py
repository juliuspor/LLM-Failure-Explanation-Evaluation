def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = min(max(value, self._lower_bound), self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    fraction = (v - self._lower_bound) / denom if denom != 0 else 0.0
    g = int(fraction * 255.0)
    g = min(max(g, 0), 255)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
    return (g, g, g)
