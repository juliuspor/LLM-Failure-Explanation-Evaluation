def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if not (0 <= g <= 255):
        raise ValueError(f"Color parameter outside of expected range: g={g}")
    return (g, g, g)