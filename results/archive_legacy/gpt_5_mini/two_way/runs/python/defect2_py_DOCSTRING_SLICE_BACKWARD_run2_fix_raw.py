def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError("Invalid bounds: upper_bound must be greater than lower_bound")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed grayscale value out of range: {g} for value={value}")
    return (g, g, g)