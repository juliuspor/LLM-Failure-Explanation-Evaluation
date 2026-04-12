def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"value {value} produced channel value {g} outside 0-255 (bounds {self._lower_bound}-{self._upper_bound})")
    r = g
    b = g
    return (r, g, b)