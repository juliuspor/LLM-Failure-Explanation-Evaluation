def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0:
        raise ValueError("Paint scale has equal lower and upper bounds")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component {g} outside range 0..255 for value {value} with bounds {self._lower_bound}..{self._upper_bound}")
    return (g, g, g)