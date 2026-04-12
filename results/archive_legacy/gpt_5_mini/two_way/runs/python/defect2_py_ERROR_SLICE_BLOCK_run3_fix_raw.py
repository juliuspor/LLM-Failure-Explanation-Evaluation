def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter 'g' outside range 0..255: {g}")
    return (g, g, g)