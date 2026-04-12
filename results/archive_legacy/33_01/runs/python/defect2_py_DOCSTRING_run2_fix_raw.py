def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    scale = (self._upper_bound - self._lower_bound)
    if scale == 0.0:
        raise ValueError("Invalid paint scale with zero range")
    g = int(round((v - self._lower_bound) / scale * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g} value={value}")
    return (g, g, g)