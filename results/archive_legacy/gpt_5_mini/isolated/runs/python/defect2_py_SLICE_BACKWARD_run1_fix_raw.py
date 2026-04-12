def get_paint(self, value: float) -> Tuple[int, int, int]:
    denom = self._upper_bound - self._lower_bound
    if denom == 0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"value out of range: {value} not in [{self._lower_bound}, {self._upper_bound}]")
    normalized = (value - self._lower_bound) / denom
    g = int(normalized * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color component out of range: g={g} (expected 0..255); value={value}, bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)