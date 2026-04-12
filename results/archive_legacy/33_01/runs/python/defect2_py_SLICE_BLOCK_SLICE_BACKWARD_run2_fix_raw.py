def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0:
        raise ValueError(f"Invalid bounds: lower_bound and upper_bound must differ (lower={self._lower_bound}, upper={self._upper_bound})")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray value out of range: g={g}, value={value}, clamped_value={v}, lower={self._lower_bound}, upper={self._upper_bound}")
    return (g, g, g)