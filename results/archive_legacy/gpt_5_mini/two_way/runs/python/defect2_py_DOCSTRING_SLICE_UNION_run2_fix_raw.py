def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("upper_bound must be different from lower_bound")
    g = int((v - self._lower_bound) / range_span * 255.0)
    r = g
    b = g
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"Color parameter outside of expected range: r={r}, g={g}, b={b}")
    return (r, g, b)