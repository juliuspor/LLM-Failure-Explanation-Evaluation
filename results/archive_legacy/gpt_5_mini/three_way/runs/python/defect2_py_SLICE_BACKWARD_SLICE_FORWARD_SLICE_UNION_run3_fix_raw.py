def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError("upper_bound and lower_bound must not be equal")
    ratio = (v - self._lower_bound) / denom
    if ratio < 0.0 or ratio > 1.0:
        raise ValueError(f"value {value} not in [{self._lower_bound}, {self._upper_bound}]")
    g = int(ratio * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component g={g} out of range 0..255 for value={value}")
    return (g, g, g)