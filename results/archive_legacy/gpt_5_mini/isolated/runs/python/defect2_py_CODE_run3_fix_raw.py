def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_ = self._upper_bound - self._lower_bound
    if range_ == 0:
        raise ValueError("Invalid bounds: upper_bound equals lower_bound")
    g = int((v - self._lower_bound) / range_ * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g} (expected 0..255) for input value={value}")
    return (g, g, g)