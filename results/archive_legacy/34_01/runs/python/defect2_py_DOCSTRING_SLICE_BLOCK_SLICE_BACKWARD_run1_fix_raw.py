def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError("Invalid bounds: upper_bound equals lower_bound (division by zero)")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    comp = int(ratio * 255.0)
    r = comp
    g = comp
    b = comp
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"Color parameter outside of expected range: r={r}, g={g}, b={b} (expected 0-255)")
    return (r, g, b)