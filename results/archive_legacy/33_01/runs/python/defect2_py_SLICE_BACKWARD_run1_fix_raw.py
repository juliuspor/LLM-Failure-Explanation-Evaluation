def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    ratio = (v - self._lower_bound) / denom
    g = int(round(ratio * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component g={g} outside 0..255 for value={value}, clamped_value={v}, lower={self._lower_bound}, upper={self._upper_bound}")
    return (g, g, g)