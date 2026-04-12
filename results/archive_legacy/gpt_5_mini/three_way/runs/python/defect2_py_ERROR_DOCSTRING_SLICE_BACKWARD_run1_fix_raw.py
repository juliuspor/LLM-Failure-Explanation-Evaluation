def get_paint(self, value: float) -> Tuple[int, int, int]:
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    frac = (v - self._lower_bound) / denom
    gray = int(round(frac * 255.0))
    r = g = b = gray
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        raise ValueError(f"Color parameter outside of expected range: r={r} g={g} b={b}")
    return (r, g, b)