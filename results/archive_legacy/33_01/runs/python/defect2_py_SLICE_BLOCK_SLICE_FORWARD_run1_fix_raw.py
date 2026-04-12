def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    try:
        g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    except Exception as e:
        raise TypeError(f"Failed to compute gray value from input {value!r}: {e}")
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range: g={g} (expected 0..255)")
    return (g, g, g)