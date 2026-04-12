def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        ratio = 0.5
    else:
        ratio = (v - self._lower_bound) / denom
    g = int(round(ratio * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside 0-255: r={g}, g={g}, b={g}")
    return (g, g, g)