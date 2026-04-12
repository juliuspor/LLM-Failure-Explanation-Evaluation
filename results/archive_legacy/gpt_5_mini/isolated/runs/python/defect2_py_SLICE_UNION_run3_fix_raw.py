def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError(f"Invalid bounds in get_paint: lower={self._lower_bound}, upper={self._upper_bound}")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: value={value}, g={g}, lower={self._lower_bound}, upper={self._upper_bound}")
    return (g, g, g)