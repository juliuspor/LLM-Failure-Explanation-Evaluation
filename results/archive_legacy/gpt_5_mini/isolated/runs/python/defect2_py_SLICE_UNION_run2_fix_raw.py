def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    normalized = (v - self._lower_bound) / denom
    normalized = max(0.0, min(1.0, normalized))
    g = int(round(normalized * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component out of range: g={g} (value={value}, bounds=({self._lower_bound},{self._upper_bound}))")
    return (g, g, g)