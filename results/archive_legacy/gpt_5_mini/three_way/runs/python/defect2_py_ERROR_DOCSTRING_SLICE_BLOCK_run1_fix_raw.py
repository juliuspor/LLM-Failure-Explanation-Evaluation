def get_paint(self, value: float) -> Tuple[int, int, int]:
    """
    Returns a paint as an RGB tuple (r, g, b) for the specified value. Each channel is in the range 0-255.
    """
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    r = g
    b = g
    if r < 0 or r > 255:
        raise ValueError(f"Red channel out of range: r={r}")
    if g < 0 or g > 255:
        raise ValueError(f"Green channel out of range: g={g}")
    if b < 0 or b > 255:
        raise ValueError(f"Blue channel out of range: b={b}")
    return (r, g, b)