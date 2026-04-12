def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    r = g
    b = g
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"RGB values must be 0..255, got r={r}, g={g}, b={b}")
    return (r, g, b)