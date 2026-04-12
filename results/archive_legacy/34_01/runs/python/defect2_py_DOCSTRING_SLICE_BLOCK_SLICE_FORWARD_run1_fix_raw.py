def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int(round((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Gray channel out of range: G={g} (expected 0-255)")
    return (g, g, g)
