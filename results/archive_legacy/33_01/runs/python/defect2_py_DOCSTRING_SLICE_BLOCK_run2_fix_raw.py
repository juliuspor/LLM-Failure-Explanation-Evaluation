def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    r = g
    b = g
    if r < 0 or r > 255:
        raise ValueError(f"Color parameter outside expected range: r={r} (expected 0..255)")
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside expected range: g={g} (expected 0..255)")
    if b < 0 or b > 255:
        raise ValueError(f"Color parameter outside expected range: b={b} (expected 0..255)")
    return (r, g, b)